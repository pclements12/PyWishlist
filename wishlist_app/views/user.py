from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.core import urlresolvers
from django.core.mail import send_mail
from wishlist_app.models import User, WishlistGroup, Invite
from wishlist_app.forms.LongRegistrationForm import LongRegistrationForm
from wishlist_app.forms.UserUpdateForm import UserUpdateForm


@login_required
@require_POST
def search(request, group_id=None):
    users = do_search(request.POST['name'])
    group = get_object_or_404(WishlistGroup, pk=group_id)
    return render(request, "wishlist_app/user/user_list.html", {"users": users, "group": group})


# helper for search in case we need it outside a form post
def do_search(name):
    print "search: %s" % name
    print "searching for user by email..."
    emails = User.objects.filter(email__iexact=name)
    print "searching for user by username..."
    users = User.objects.filter(username__icontains=name)
    return users | emails


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
                print "invite scrubbed from db, key removed from session"
            except Invite.DoesNotExist:
                print "Invalid or already used activation key. User not added to a group"
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
    inv = Invite.objects.create(email=request.POST['email'], group=group, by=request.user)
    print "Invite created [%s]" % inv
    send_invite_email(request, inv, group)
    return HttpResponse("Invite sent")


def send_invite_email(request, inv, group):
    path = generate_invite_link(inv)
    print "send invite email for %s @ %s" % (inv, path)
    url = request.build_absolute_uri(path)
    print "Absolute url: %s" % url
    message = """
        You've been invited by %s to join '%s'--a Wishlist Group!
        Follow this link to activate your invitation and join in:
        %s

        Happy Wishing!

        The Wishlist Team

    """ % (request.user, group.name, url)
    send_mail("You've been invited to a Wishlist!", message, 'info@pywishlist.com', [inv.email], fail_silently=True)


def generate_invite_link(inv):
    url = "%s?activation_key=%s" % (urlresolvers.reverse("register"), inv.key)
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