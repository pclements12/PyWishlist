from django.shortcuts import get_object_or_404, render, redirect
from wishlist_app.models import User, WishlistGroup, Invite
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.http import HttpResponse, JsonResponse, Http404
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse


@login_required
@require_POST
def search(request, group_id=None):
    users = do_search(request.POST['name'])
    group = get_object_or_404(WishlistGroup, pk=group_id)
    return render(request, "wishlist_app/user/user_list.html", {"users": users, "group": group})


def do_search(name):
    print "search: %s" % name
    print "searching for user by email..."
    users = User.objects.filter(email=name)
    if not users.exists():
        print "%s email not found"
        print "searching for user by username..."
        users = User.objects.filter(username=name)
    return users


@require_http_methods(['GET', 'POST'])
def register(request):
    print "Register: %s" % request
    if request.POST:
        print "Check if user was invited to a group"
        print "Activation key? %s" % request.session['activation_key']
        key = request.session['activation_key']
        print "Post Registration form"
        form = UserCreationForm(request.POST)
        print "Creating user..."
        user = form.save()
        print "New user created: %s" % user
        auth_user = authenticate(username=user.username, password=request.POST['password2'])
        print "authenticating user..."
        login(request, auth_user)
        print "Check if user was invited to a group"
        print "Activation key? %s" % request.session['activation_key']
        if key is not None:
            try:
                inv = Invite.objects.get(key=key)
                print "Update user email with invite email %s" % inv.email
                user.email = inv.email
                user.save()
                inv.group.add_user(user)
                print "User successfully added to invite group %s" % inv.group
                inv.delete()
                del request.session['activation_key']
                print "invite scrubbed from db, key removed from session"
            except Invite.DoesNotExist:
                print "Invalid or already used activation key. User not added to a group"
        return redirect("wishlists")
    # GET:
    print "Checking for activation key %s" % request.GET['activation_key']
    request.session['activation_key'] = request.GET['activation_key']
    print "Get Registration form"
    form = UserCreationForm()
    print "form created"
    return render(request, 'wishlist_app/register.html', {"form": form})


@login_required
@require_POST
def invite(request):
    print "request to invite %s" % request.POST
    group = get_object_or_404(WishlistGroup, pk=request.POST['group_id'])
    print "found group %s" % group
    if not group.contains_user(request.user.id):
        raise PermissionDenied("Can't invite people to a group if you aren't in it")
    print "requesting user belongs to the group %s" % request.user
    inv = Invite.objects.create(email=request.POST['email'], group=group)
    print "Invite created %s" % inv
    send_invite_email(request, inv)
    return HttpResponse("Invite sent")


def send_invite_email(request, inv):
    path = generate_invite_link(inv)
    print "send invite email for %s @ %s" % (inv, path)
    url = request.build_absolute_uri(path)
    print "Absolute url: %s" % url


def generate_invite_link(inv):
    url = "%s?activation_key=%s" % (reverse("register"), inv.key)
    print "Registration url: %s" % url
    return url

# json example:
# from django.forms.models import model_to_dict
# import json
# data = model_to_dict(user, fields=('username', 'id'))
# return HttpResponse(json.dumps(data), content_type='application/json')



#
# def require_user_can_edit_item(**map):
#     print "map: %s" % map
#     if "index" in map:
#         index = map['index']
#     else:
#         raise Exception("args index of item id must be specified")
#
#         def decorator(func):
#             def new_method(request, *args, **kwargs):
#                 item = get_object_or_404(Item, pk=args[index])
#                 if item.user != request.user:
#                     raise PermissionDenied
#                 return func(request, *args, **kwargs)
#             return new_method
#         return decorator
#
