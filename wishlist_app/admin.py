from django.contrib import admin

# Register your models here.

from .models import Item, WishlistGroup, GroupMember, Role, Invite, RegistryAssignment, SecretSantaAssignment


admin.site.register(Item)
admin.site.register(WishlistGroup)
admin.site.register(GroupMember)
admin.site.register(Role)
admin.site.register(Invite)
admin.site.register(RegistryAssignment)
admin.site.register(SecretSantaAssignment)
