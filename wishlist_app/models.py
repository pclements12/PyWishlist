from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import PermissionDenied, ValidationError
import uuid

# Create your models here.
# Base module


class DBObject(models.Model):
    created_date = models.DateTimeField(default=datetime.now)
    modified_date = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, related_name='%(class)s_created_by', default=None, blank=True, null=True)
    modified_by = models.ForeignKey(User, related_name='%(class)s_modified_by', default=None, blank=True, null=True)

    class Meta:
        abstract = True


# Do we extend user to have some custom attributes? like display name, maybe an avatar?


class Role(DBObject):
    # wishlist group
    # user
    # role (admin, member)
    pass


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

    def remove_user(self, user):
        if self.contains_user(user):
            GroupMember.objects.get(user=user, group=self).delete()
        else:
            raise PermissionDenied("User isn't a member of the group")

    def remove_user(self, user):
        print "removing user from group %s" % user
        GroupMember.objects.get(user=user, group=self).delete()
        items = Item.objects.filter(wisher=user, group=self)
        print "deleting user's items from the group"
        for i in items:
            print "delete item %s" % i
            i.delete()
        print "unclaim items for user"
        items = Item.objects.filter(giver=user)
        for i in items:
            print "unclaiming item %s" % i
            i.unclaim()

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
        return self.created != self.modified

    def __str__(self):
        return "%s:'%s'" % (self.commenter.username, self.text)


class Item(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(default=None, null=True, blank=True)
    link = models.URLField(default=None, null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    group = models.ForeignKey(WishlistGroup, related_name="wishlist_group", on_delete=models.CASCADE)
    wisher = models.ForeignKey(User, related_name="wishlist_wisher")
    giver = models.ForeignKey(User, related_name="wishlist_giver", default=None, blank=True, null=True)
    claimed = models.BooleanField(default=False)
    comments = models.ManyToManyField(Comment, through="ItemComment")

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
            raise PermissionDenied("Item has already been claimed")
        if user == self.wisher:
            raise PermissionDenied("User's can't claim their own items")
        assignment = self.group.get_assignment(user)
        if self.group.is_secret_santa():
            if assignment.wisher != self.wisher:
                raise PermissionDenied("User must be the wisher's secret santa to claim their items")
        elif self.group.is_registry():
            if self.wisher != assignment.wisher:
                raise PermissionDenied("Can only claim items of the registry's target user")

    def __str__(self):
        if self.giver is None:
            return "%s (%s)" % (self.name, self.wisher.username)
        return "%s (%s<-%s)" % (self.name, self.wisher.username, self.giver.username)


class ItemComment(models.Model):
    item = models.ForeignKey(Item, related_name="itemcomment_item", null=False)
    comment = models.ForeignKey(Comment, related_name="itemcomment_comment")


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
    giver = models.ForeignKey(User, related_name="santa_giver", null=True, default=None)

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

