from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.core import urlresolvers
from django.core.mail import send_mail
from datetime import datetime
from wishlist_app.models import User, WishlistGroup, Invite, Item
from wishlist_app.forms.LongRegistrationForm import LongRegistrationForm
from wishlist_app.forms.UserUpdateForm import UserUpdateForm


@login_required
@require_POST
def search(request, group_id=None):
    users = do_search(request.POST['name'])[:10]
    group = get_object_or_404(WishlistGroup, pk=group_id)
    return render(request, "wishlist_app/user/user_list.html", {"users": users, "group": group})


# helper for search in case we need it outside a form post
def do_search(name):
    print "search: %s" % name
    print "searching for user by email..."
    emails = User.objects.filter(email__iexact=name)
    print "searching for user by username..."
    users = User.objects.filter(username__icontains=name).order_by('username')
    return users | emails


@login_required
def wishlist(request):
    items = Item.objects.filter(wisher=request.user).order_by('name')
    return render (request, "wishlist_app/item/my_wishlist.html", {"items": items})


@login_required
def profile(request):
    group_count = len(WishlistGroup.get_groups_by_user(request.user))
    invite_count = len(Invite.objects.filter(inviter=request.user))
    return render(request, "wishlist_app/user/profile.html",
                  {"user": request.user,
                   "group_count": group_count,
                   "invite_count": invite_count})


@require_http_methods(['GET', 'POST'])
def register(request):
    print "Register: %s" % request
    if request.POST:
        print "Check if user was invited to a group"
        key = None
        if 'activation_key' in request.session:
            key = request.session['activation_key']
            print "Session activation key? %s" % key
        form = LongRegistrationForm(request.POST)
        if not form.is_valid():
            return render(request, 'wishlist_app/register.html', {"form": form})
        print "Creating user..."
        user = form.save()
        print "New user created: %s" % user
        auth_user = authenticate(username=user.username, password=request.POST['password2'])
        print "authenticating user..."
        login(request, auth_user)
        print "Check if user was invited to a group"
        if key is not None:
            try:
                print "Activation key? %s" % key
                inv = Invite.objects.get(key=key, used=False)
                user.save()
                inv.group.add_user(user)
                print "User successfully added to invite group %s" % inv.group
                inv.used = True
                inv.save()
                if 'activation_key' in request.session:
                    del request.session['activation_key']
                print "invite used, activation key removed from session"
                return redirect("group_home", inv.group.id)
            except Invite.DoesNotExist:
                print "Invalid or already used invite activation key. User not added to a group"
        else:
            print "no invite for the user"
        return redirect("wishlists")
    # GET:
    print "Checking for activation key"
    if 'activation_key' in request.GET:
        print "activation key provided: %s" % request.GET['activation_key']
        request.session['activation_key'] = request.GET['activation_key']
    print "Get Registration form"
    form = LongRegistrationForm()
    print "form created"
    return render(request, 'wishlist_app/register.html', {"form": form})


@login_required
@require_POST
def invite(request):
    print "request to invite %s" % request.POST
    group = get_object_or_404(WishlistGroup, pk=request.POST['group_id'])
    print "found group %s" % group
    if not group.contains_user(request.user):
        raise PermissionDenied("Can't invite people to a group if you aren't in it")
    print "requesting user belongs to the group %s" % request.user

    if Invite.objects.filter(inviter=request.user, created_date=datetime.today()).count() > 15:
        return PermissionDenied("Maximum invites reached")

    inv = Invite.objects.create(email=request.POST['email'], group=group, inviter=request.user)
    print "Invite created [%s]" % inv
    send_invite_email(request, inv)
    return HttpResponse("Invite sent")


def view_html_invite(request, inv_id):
    inv = get_object_or_404(Invite, pk=inv_id)
    url = generate_invite_link(request, inv)
    return HttpResponse(render_to_string('emails/invite.html', {'inv': inv, 'url': url}))


def send_invite_email(request, inv):
    url = generate_invite_link(request, inv)

    print "Absolute url: %s" % url

    msg_plain = render_to_string('emails/invite.txt', {'inv': inv, 'url': url})
    msg_html = render_to_string('emails/invite.html', {'inv': inv, 'url': url})

    print "generated html and plain text emails for delivery"

    send_mail(
        "You've been invited to a Wishlist!",
        msg_plain,
        inv.inviter.email,
        [inv.email],
        html_message=msg_html,
        fail_silently=True
    )
    print "invite sent from %s to %s" % (inv.inviter.email, inv.email)


def generate_invite_link(request, inv):
    path = "%s?activation_key=%s" % (urlresolvers.reverse("register"), inv.key)
    print "send invite email for %s @ %s" % (inv, path)
    url = request.build_absolute_uri(path)
    print "Registration url: %s" % url
    return url


@login_required
@require_http_methods(["GET", "POST"])
def update(request):
    print "Update user: %s" % request.user
    if request.POST:
        print "posted values %s" % request.POST
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if not user_form.is_valid():
            return render(request, 'wishlist_app/user/user_update.html', {'user_form': user_form})
        user = user_form.save()
        print "updated user %s" % user
        return redirect("user_profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        return render(request, 'wishlist_app/user/user_update.html', {'user_form': user_form})


@login_required
@require_POST
def remove(request, group_id):
    print "Request by %s to leave group %s" % (request.user, group_id)
    group = get_object_or_404(WishlistGroup, pk=group_id)
    group.remove_user(request.user)
    print "remove user from group"
    return redirect("wishlists")

