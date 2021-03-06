from django.conf.urls import url
from .views import item, group_item, operations, group, user, member, comment

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
    url(r'^group/(?P<group_id>[0-9]+)/clone/?$', group.clone, name="group_clone"),

    # group member operations
    url(r'^(?P<group_id>[0-9]+)/user/(?P<wisher_id>[0-9]+)/$', group.user_wishlist, name="user_wishlist"),
    url(r'^group/(?P<group_id>[0-9]+)/add$', group.add_members, name="member_add"),
    url(r'^group/(?P<group_id>[0-9]+)/add/(?P<user_id>[0-9]+)$', member.add, name="add_user"),
    url(r'^group/member/remove/(?P<member_id>[0-9]+)$', member.delete, name="remove_user"),

    # item operations (from personal wishlist)
    url(r'^user/wishlist$', user.wishlist, name="my_wishlist"),
    url(r'^item/$', item.create, name="item_create"),
    url(r'^item/(?P<item_id>[0-9]+)/?$', item.read, name="item_read"),
    url(r'^item/(?P<item_id>[0-9]+)/edit/?$', item.update, name="item_update"),
    url(r'^item/(?P<item_id>[0-9]+)/delete/?$', item.delete, name="item_delete"),

    # group item operations (from a group)
    url(r'^group/(?P<group_id>[0-9]+)/item/$', group_item.create, name="group_item_create"),
    url(r'^group/(?P<group_id>[0-9]+)/item/(?P<item_id>[0-9]+)/?$', group_item.read, name="group_item_read"),
    url(r'^group/(?P<group_id>[0-9]+)/item/(?P<item_id>[0-9]+)/claim/?$',
        group_item.claim, name="group_item_claim"),
    url(r'^group/(?P<group_id>[0-9]+)/item/(?P<item_id>[0-9]+)/unclaim/?$',
        group_item.unclaim, name="group_item_unclaim"),
    url(r'^group/(?P<group_id>[0-9]+)/items/', group_item.list, name='group_items'),

    # comment
    url(r'^comment/(?P<comment_id>[0-9]+)/delete', comment.delete, name="comment_delete"),
    url(r'^group/(?P<group_id>[0-9]+)/item/(?P<item_id>[0-9]+)/comment$',
        group_item.comment, name="item_comment"),
    url(r'^comment/(?P<comment_id>[0-9]+)/edit$',
        group_item.edit_comment, name="item_comment_edit"),

    # user
    url(r'^user$', user.profile, name="user_profile"),
    url(r'^user/edit$', user.update, name="user_update"),
    url(r'^user/remove/(?P<group_id>[0-9]+)$', user.remove, name="user_remove"),
    url(r'^user/search/(?P<group_id>[0-9]+)$', user.search, name="user_search"),
    url(r'^user/invite', user.invite, name="user_invite"),

    # testing
    url(r'^invite/(?P<inv_id>[0-9]+)$', user.view_html_invite, name="user_invite_view"),
]
