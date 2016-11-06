from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.db.models import Q
import uuid
import bleach


class DBObject(models.Model):
    created_date = models.DateTimeField(default=datetime.now)
    modified_date = models.DateTimeField(default=datetime.now)

    class Meta:
        abstract = True


def follow_through(queryset, field):
    items = []
    for item in queryset.all():
        items.append(getattr(item, field))
    return items


def full_name_display(self):
    """
        Monkey patch method for built in User object
        if the full name is present, return surrounded by parens, otherwise return empty string
    :return:
    """
    if self.get_full_name():
        return "(%s)" % self.get_full_name()
    return ""

# user methods
# monkey patch in a display method for user names
User.get_full_name_display = full_name_display


def get_user_groups(self):
    members = GroupMember.objects.filter(user=self).prefetch_related("group")
    return follow_through(members, "group")

User.get_group_list = get_user_groups


class Item(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(default=None, null=True, blank=True)
    link = models.URLField(default=None, null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    wisher = models.ForeignKey(User, related_name="wishlist_wisher")
    giver = models.ForeignKey(User, related_name="wishlist_giver", default=None, blank=True, null=True)
    claimed = models.BooleanField(default=False)

    groups = models.ManyToManyField('WishlistGroup', through='GroupItem')

    def claim(self, user):
        self.giver = user
        self.claimed = True
        self.save()

    def unclaim(self):
        self.giver = None
        self.claimed = False
        self.save()

    def check_claim(self, user):
        if self.giver is not None:
            print "Item has already been claimed"
            raise PermissionDenied("Item has already been claimed")
        if user == self.wisher:
            print "Can't claim own item"
            raise PermissionDenied("User's can't claim their own items")
        # check if item is in a group that the user belongs to

        user_in_group = False
        user_groups = user.get_group_list()
        for grp in self.groups.all():
            print "Item group %s" % grp.id
            for user_grp in user_groups:
                print "User group %s" % user_grp.id
                if grp.id == user_grp.id:
                    print "User and item group match"
                    user_in_group = True
                    break
            if user_in_group:
                break
        if not user_in_group:
            print "User is not in a group with this item"
            raise PermissionDenied("User is not in a group that this item belongs to")

    def remove(self):
        # need to delete item comments before we can delete the item
        # Item -> GroupItem -> ItemComment -> Comment
        print "deleting item %s" % self.id
        group_items = GroupItem.objects.filter(item=self)
        print "found %s group items" % len(group_items)
        for i in group_items:
            comments = ItemComment.objects.filter(group_item=i)
            print "found %s comments" % len(comments)
            for c in comments:
                print "deleting comment %s" % c
                c.delete()
            i.delete()
        self.delete()

    def __str__(self):
        if self.giver is None:
            return "%s (%s)" % (self.name, self.wisher.username)
        return "%s (%s<-%s)" % (self.name, self.wisher.username, self.giver.username)


class WishlistGroup(models.Model):
    name = models.CharField(max_length=200, default=None)
    description = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(User, related_name="group_creator", default=None)
    end_date = models.DateField(default=None, blank=True, null=True)
    users = models.ManyToManyField(User, through='GroupMember')
    # include this so we can compare with WishlistGroup.REGULAR for example
    REGULAR = "regular"
    SECRET_SANTA = "secret_santa"
    REGISTRY = "registry"
    GROUP_TYPES = ((REGULAR, "Individual Wishlists"), (SECRET_SANTA, "Secret Santa"), (REGISTRY, 'Registry/Birthday'))
    type = models.CharField(max_length=30, choices=GROUP_TYPES, default=REGULAR)

    items = models.ManyToManyField(Item, through='GroupItem')

    @staticmethod
    def get_groups_by_user(user):
        # return user.groups
        group_members = GroupMember.objects.filter(user=user)
        group_ids = map(lambda member: member.group.id, group_members)
        return WishlistGroup.objects.filter(id__in=group_ids)

    def members(self):
        return GroupMember.objects.filter(group=self).order_by("user__username")

    def add_user(self, user):
        return GroupMember.objects.create(user=user, group=self)

    def clone_group(self, name):
        new_group = WishlistGroup.objects.get(pk=self.pk)
        new_group.pk = None
        new_group.name = name
        new_group.save()

    def remove_user(self, user):
        print "removing user from group %s" % user
        if not self.contains_user(user):
            raise PermissionDenied("User isn't a member of the group")

        items = GroupItem.objects.filter(item__wisher=user, group=self)
        print "deleting user's group-items from the group"
        for gi in items:
            print "delete group-item %s" % gi
            if self.contains_user(gi.item.giver):
                print "unclaim user's group item claimed by a member of this group %s" % gi.item
                gi.item.unclaim()
            gi.delete()
        print "unclaim items for %s" % user
        # what if a giver is in multiple groups with them?
        group_items = GroupItem.objects.filter(group=self, item__giver=user)
        for gi in group_items:
            print "unclaiming item %s" % gi
            gi.item.unclaim()
        GroupMember.objects.get(user=user, group=self).delete()
        print "user successfully removed from group"

    def remove_all_users(self):
        members = GroupMember.objects.filter(group=self)
        for m in members:
            self.remove_user(m.user)

    def remove_group(self):
        print "deleting group comments"
        group_items = GroupItem.objects.filter(group=self)
        for gi in group_items:
            gi.comments.all().delete()
        print "deleting group memberships"
        self.remove_all_users()
        print "deleting group"
        self.delete()
        print "group delete"

    def contains_user(self, user):
        for member in self.members():
            if member.user == user:
                return True
        return False

    # for a secret-santa type group, create any missing assignments
    def create_secret_santa_assignments(self):
        if not self.type == self.SECRET_SANTA:
            return
        for user in self.users.all():
            try:
                SecretSantaAssignment.objects.get(group=self, wisher=user)
            except SecretSantaAssignment.DoesNotExist:
                SecretSantaAssignment.objects.create(group=self, wisher=user)

    def get_assignment(self, user):
        if self.type == self.REGULAR:
            return None
        if self.is_secret_santa():
            try:
                ass = SecretSantaAssignment.objects.get(group=self, giver=user)
                if ass.wisher is not None:
                    return ass
                return None
            except SecretSantaAssignment.DoesNotExist:
                return None
        elif self.is_registry():
            try:
                return RegistryAssignment.objects.get(group=self)
            except RegistryAssignment.DoesNotExist:
                return None
        return None

    def has_assignments(self):
        if self.is_secret_santa():
            try:
                ass = SecretSantaAssignment.objects.filter(~Q(giver=None), group=self)
                return len(ass.all()) > 0
            except SecretSantaAssignment.DoesNotExist:
                return False
        elif self.is_registry():
            try:
                ass = RegistryAssignment.objects.filter(group=self)
                return len(ass.all()) > 0
            except RegistryAssignment.DoesNotExist:
                return False
        return False

    def is_regular(self):
        return self.type == self.REGULAR

    def is_secret_santa(self):
        return self.type == self.SECRET_SANTA

    def is_registry(self):
        return self.type == self.REGISTRY

    def __str__(self):
        return self.name


class Comment(models.Model):
    created = models.DateTimeField(verbose_name="Created Date", auto_now_add=True)
    modified = models.DateTimeField(verbose_name="Modified Date", auto_now=True)
    commenter = models.ForeignKey(User, related_name="comment_commenter", null=False)
    anonymous = models.BooleanField(default=False)
    hide_from_wisher = models.BooleanField(default=False)

    text = models.TextField()

    def is_edited(self):
        timediff = self.modified - self.created
        # 30 seconds for ninja edits :)
        return timediff.total_seconds() > 30

    def __str__(self):
        return "%s:'%s'" % (self.commenter.username, self.text)

    allowed_tags = bleach.ALLOWED_TAGS + ['br', 'img']
    allowed_attrs = dict(bleach.ALLOWED_ATTRIBUTES)
    allowed_attrs['img'] = ["src", "title", "alt"]

    def markup_text(self):
        # convert new lines in comments to breaks
        replaced = self.text.replace("\n", "<br/>")
        # clean any potentially malicious html/scripts
        return bleach.clean(replaced, tags=self.allowed_tags, attributes=self.allowed_attrs, strip=True)


class GroupComment(models.Model):
    group = models.ForeignKey(WishlistGroup, related_name="groupcomment_group", null=False)
    comment = models.ForeignKey(WishlistGroup, related_name="groupcomment_comment", null=False)


class GroupMember(models.Model):
    group = models.ForeignKey(WishlistGroup, related_name="group_member_wishlistgroup", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="group_member_user")

    class Meta:
        unique_together = ("group", "user")

    def __str__(self):
        return "%s:%s" % (self.group, self.user)


class GroupItem(models.Model):
    group = models.ForeignKey(WishlistGroup, related_name="group_item_wishlistgroup", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="group_item_item", on_delete=models.CASCADE)
    comments = models.ManyToManyField(Comment, through="ItemComment")

    def __str__(self):
        return "%s:%s" % (self.group, self.item)


class ItemComment(models.Model):
    group_item = models.ForeignKey(GroupItem, related_name="itemcomment_group_item")
    comment = models.ForeignKey(Comment, related_name="itemcomment_comment")

    def __str__(self):
        return "%s:%s" % (self.group_item, self.comment)

def generate_uuid():
    return uuid.uuid1()


class Invite(models.Model):
    inviter = models.ForeignKey(User, related_name='invited_by')
    created_date = models.DateField(default=timezone.now)
    group = models.ForeignKey(WishlistGroup, related_name="invite_group", on_delete=models.CASCADE)
    key = models.CharField(max_length=64, verbose_name=u"Activation key", default=generate_uuid, null=False)
    email = models.EmailField(null=False)
    used = models.BooleanField(default=False)

    def __str__(self):
        return "Invite by %s: %s to %s (%s) on %s" % (self.inviter, self.group, self.email, self.key, self.created_date)


class SecretSantaAssignment(models.Model):
    group = models.ForeignKey(WishlistGroup, related_name="santa_group", null=False, on_delete=models.CASCADE)
    wisher = models.ForeignKey(User, related_name="santa_wisher", null=False)
    giver = models.ForeignKey(User, related_name="santa_giver", null=True, default=None, blank=True)

    def __str__(self):
        return "Group: %s, Wisher: %s, Giver: %s" % (self.group, self.wisher, self.giver)

    class Meta:
        unique_together = ("group", "wisher", "giver")


class RegistryAssignment(models.Model):
    group = models.OneToOneField(WishlistGroup, related_name="registry_group", null=False, on_delete=models.CASCADE)
    wisher = models.ForeignKey(User, related_name="registry_wisher", null=False)

    def __str__(self):
        return "Group: %s, Wisher: %s" % (self.group, self.wisher)

    class Meta:
        unique_together = ("group", "wisher")
