from django.shortcuts import  get_object_or_404, redirect
from wishlist_app.models import WishlistGroup, User, GroupMember
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied, ValidationError


@login_required
@require_POST
def add(request, group_id, user_id):
    group = get_object_or_404(WishlistGroup, pk=group_id)
    user = get_object_or_404(User, pk=user_id)
    if not group.contains_user(request.user):
        raise PermissionDenied
    if group.contains_user(user):
        raise ValidationError("User is already a member of this group")
    group.add_user(user)
    return HttpResponse()


@login_required
@require_POST
def delete(request, member_id):
    member = get_object_or_404(GroupMember, pk=member_id)
    if request.user != member.group.creator:
        raise PermissionDenied
    if request.user == member.user:
        raise PermissionDenied("Creator can't be removed. Delete the group to remove it")
    member.group.remove_user(member.user)
    return redirect("group_home", member.group.id)


