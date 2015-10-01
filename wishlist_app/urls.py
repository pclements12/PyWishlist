from django.conf.urls import url
from .views import item, operations, group, user, member

urlpatterns = [
    # url(r'^accounts/login/$', operations.user_login, name="login"),
    # all wishlists
    url(r'^user/register$', user.register, name='register'),
    url(r'^logout$', operations.do_logout, name='logout'),
    url(r'^$', operations.wishlists, name='wishlists'),

    # group operations
    url(r'^(?P<group_id>[0-9]+)/$', group.home, name="group_home"),
    url(r'^group/$', group.create, name="group_create"),
    url(r'^group/(?P<group_id>[0-9]+)/edit/?$', group.update, name="group_update"),
    url(r'^group/(?P<group_id>[0-9]+)/delete/?$', group.delete, name="group_delete"),
    url(r'^group/(?P<group_id>[0-9]+)/assignments/?$', group.assignments, name="group_assignments"),

    # group member operations
    url(r'^(?P<group_id>[0-9]+)/user/(?P<wisher_id>[0-9]+)/$', group.user_wishlist, name="user_wishlist"),
    url(r'^group/(?P<group_id>[0-9]+)/add$', group.add_members, name="member_add"),
    url(r'^group/(?P<group_id>[0-9]+)/add/(?P<user_id>[0-9]+)$', member.add, name="add_user"),
    url(r'^group/member/remove/(?P<member_id>[0-9]+)$', member.delete, name="remove_user"),

    # wishlist item operations
    url(r'^(?P<group_id>[0-9]+)/item/$', item.create, name="item_create"),
    url(r'^item/(?P<item_id>[0-9]+)/?$', item.read, name="item_read"),
    url(r'^item/(?P<item_id>[0-9]+)/edit/?$', item.update, name="item_update"),
    url(r'^item/(?P<item_id>[0-9]+)/delete/?$', item.delete, name="item_delete"),
    url(r'^item/(?P<item_id>[0-9]+)/claim/?$', item.claim, name="item_claim"),
    url(r'^item/(?P<item_id>[0-9]+)/unclaim/?$', item.unclaim, name="item_unclaim"),

    # user
    url(r'^user/search/(?P<group_id>[0-9]+)$', user.search, name="user_search"),
    url(r'^user/invite', user.invite, name="user_invite"),
]
