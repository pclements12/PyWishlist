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

    @staticmethod
    def get_groups_by_user(user):
        # return user.groups
        group_members = GroupMember.objects.filter(user=user)
        group_ids = map(lambda member: member.group.id, group_members)
        return WishlistGroup.objects.filter(id__in=group_ids)

    def add_user(self, user):
        return GroupMember.objects.create(user=user, group=self)

    def contains_user(self, user_id):
        print "Check if group contains user:  %s" % user_id
        try:
            user = User.objects.get(pk=user_id)
            print "Found user: %s" % user_id
            print "Searching group list for user: %s" % self.users
            for u in self.users.all():
                if u == user:
                    return True
            return False
        except User.DoesNotExist:
            return False

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(default=None, null=True, blank=True)
    link = models.URLField(default=None, null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    group = models.ForeignKey(WishlistGroup, related_name="wishlist_group")
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
    group = models.ForeignKey(WishlistGroup, related_name="group_member_wishlistgroup")
    user = models.ForeignKey(User, related_name="group_member_user")

    class Meta:
        unique_together = ("group", "user")

    def __str__(self):
        return "%s:%s" % (self.group, self.user)


def generate_uuid():
    return uuid.uuid1()


class Invite(models.Model):
    group = models.ForeignKey(WishlistGroup, related_name="invite_group")
    key = models.CharField(max_length=64, verbose_name=u"Activation key", default=generate_uuid, null=False)
    email = models.EmailField(null=False)

    def __str__(self):
        return "Invite: %s to %s (%s)" % (self.group, self.email, self.key)




