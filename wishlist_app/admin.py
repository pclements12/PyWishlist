from django.contrib import admin

# Register your models here.

from .models import Item, WishlistGroup, GroupMember, Role


admin.site.register(Item)
admin.site.register(WishlistGroup)
admin.site.register(GroupMember)
admin.site.register(Role)
