from django.shortcuts import  get_object_or_404, redirect
from wishlist_app.models import WishlistGroup, User, GroupMember
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core import urlresolvers


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
    _notify_added_user(request, group, user, request.user)
    return HttpResponse()


def _notify_added_user(request, group, user, adder):
    print "sending group add notification email"
    path = urlresolvers.reverse("group_home", kwargs={'group_id': group.id})
    url = request.build_absolute_uri(path)

    msg_plain = render_to_string('emails/add_member.txt', {'group': group, 'user': user, 'adder': adder, 'url': url})
    msg_html = render_to_string('emails/add_member.html', {'group': group, 'user': user, 'adder': adder, 'url': url})

    print "generated html and plain text emails for delivery"
    try:
        send_mail(
            "You've been added to a Wishlist!",
            msg_plain,
            adder.email,
            [user.email],
            html_message=msg_html,
            fail_silently=True
        )
    except Exception:
        # not sure why we need to do this...fails even when fail_silently=True
        pass
    return


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


