from django.contrib import admin

# Register your models here.

from .models import Item, WishlistGroup, GroupMember, Invite, RegistryAssignment, \
    SecretSantaAssignment, Comment, ItemComment, GroupComment, GroupItem


class GroupItemInline(admin.TabularInline):
    model = GroupItem


class ItemAdmin(admin.ModelAdmin):
    inlines = [GroupItemInline, ]


admin.site.register(Item, ItemAdmin)
admin.site.register(WishlistGroup)
admin.site.register(GroupMember)
admin.site.register(Invite)
admin.site.register(RegistryAssignment)
admin.site.register(SecretSantaAssignment)
admin.site.register(Comment)
admin.site.register(ItemComment)
admin.site.register(GroupComment)
admin.site.register(GroupItem)
