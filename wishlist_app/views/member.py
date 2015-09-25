from django.shortcuts import  get_object_or_404
from wishlist_app.models import WishlistGroup, User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied, ValidationError


@login_required
@require_POST
def add(request, group_id, user_id):
    group = get_object_or_404(WishlistGroup, pk=group_id)
    if not group.contains_user(request.user.id):
        raise PermissionDenied
    if group.contains_user(user_id):
        raise ValidationError("User is already a member of this group")
    user = get_object_or_404(User, pk=user_id)
    group.add_user(user)
    return HttpResponse()


