from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import uuid

# Create your models here.
# Base module


class DBObject(models.Model):
    created_date = models.DateTimeField(default=datetime.now())
    modified_date = models.DateTimeField(default=datetime.now())
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
        print "Check if group contains user:  %s" % user
        print "Searching group list for user: %s" % self.members()
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

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(default=None, null=True, blank=True)
    link = models.URLField(default=None, null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    group = models.ForeignKey(WishlistGroup, related_name="wishlist_group", on_delete=models.CASCADE)
    wisher = models.ForeignKey(User, related_name="wishlist_wisher")
    giver = models.ForeignKey(User, related_name="wishlist_giver", default=None, blank=True, null=True)
    claimed = models.BooleanField(default=False)

    def claim(self, user):
        self.giver = user
        self.claimed = True
        self.save()

    def unclaim(self):
        self.giver = None
        self.claimed = False
        self.save()

    def __str__(self):
        if self.giver is None:
            return "%s (%s)" % (self.name, self.wisher.username)
        return "%s (%s<-%s)" % (self.name, self.wisher.username, self.giver.username)


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
    group = models.ForeignKey(WishlistGroup, related_name="invite_group", on_delete=models.CASCADE)
    key = models.CharField(max_length=64, verbose_name=u"Activation key", default=generate_uuid, null=False)
    email = models.EmailField(null=False)

    def __str__(self):
        return "Invite: %s to %s (%s)" % (self.group, self.email, self.key)


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


