from wishlist_app.forms.GroupForm import GroupForm
from django.shortcuts import render, get_object_or_404, redirect
from wishlist_app.models import GroupMember, WishlistGroup, Item, User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.core.exceptions import PermissionDenied


@login_required(login_url="login")
def home(request, group_id):
    group = get_object_or_404(WishlistGroup, pk=group_id)
    context = {
        "wishes": Item.objects.filter(group=group, wisher=request.user),
        "gives": Item.objects.filter(group=group, giver=request.user),
        "group": group,
        "members": GroupMember.objects.filter(group=group)
    }
    # display two lists:
    # 1. what you wished for
    # -option to add a wished item
    # 2. what you've committed to buy for others
    # -option to browse wished items
    # 3. List of wishes grouped by user?
    return render(request, "wishlist_app/group/group_home.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def create(request):
    print "%s is wants to create a new group" % request.user
    if request.POST:
        print "posted values %s" % request.POST
        group_form = GroupForm(request.POST)
        # get unsaved reference to a group model
        group = group_form.save(commit=False)
        # add the owner field (required)
        group.creator = request.user
        group.save()
        # add the owner as a member of the group
        GroupMember.objects.create(user=request.user, group=group)
        print "created a new group %s" % group
        return redirect("group_home", group.id)
    else:
        group_form = GroupForm()
        return render(request, 'wishlist_app/group/new_group.html', {'group_form': group_form})


@login_required
@require_http_methods(["GET", "POST"])
def update(request, group_id):
    group = get_object_or_404(WishlistGroup, pk=group_id)
    if request.user != group.creator:
        print "user is not allowed to edit this group"
        raise PermissionDenied("Only the creator can edit an group")

    print "Update group: %s" % group
    if request.POST:
        print "posted values %s" % request.POST
        group.name = request.POST['name']
        group.description = request.POST['description']
        group.save()
        print "update group %s" % group
        return redirect("group_home", group.id)
    else:
        group_form = GroupForm(instance=group)
        return render(request, 'wishlist_app/group/update_group.html', {'group_form': group_form, 'group': group})


@login_required
@require_http_methods(["GET", "POST"])
def add_members(request, group_id):
    group = get_object_or_404(WishlistGroup, pk=group_id)
    return render(request, 'wishlist_app/members/add_members.html', {'group': group})


@login_required
@require_POST
def delete(request, group_id):
    print "reading group %s" % group_id
    group = get_object_or_404(WishlistGroup, pk=group_id)
    if request.user != group.creator:
        print "user is not allowed to delete this group"
        raise PermissionDenied("Only the creator can delete a group")
    print "got group %s" % group
    print "Cleaning up items and members of the group: %s" % group.name
    members = GroupMember.objects.filter(group=group)
    for m in members:
        print "Deleting members of group: %s" % m.user.username
        m.delete()
    items = Item.objects.filter(group=group)
    for i in items:
        print "deleting item from group: %s" %i.name
        i.delete()
    group.delete()
    print "Successfully deleted group"
    return redirect("wishlists")


@login_required
def wishlist_members(request, group_id):
    group = get_object_or_404(WishlistGroup, pk=group_id)
    users = group.users()
    return render(request, "wishlist_app/group/wishlist_members.html", {
        "members": users,
        "group": group
    })


@login_required
def user_wishlist(request, group_id, wisher_id):
    group = get_object_or_404(WishlistGroup, pk=group_id)
    wisher = get_object_or_404(User, pk=wisher_id)
    print "Wisher: %s: %s" % (wisher_id, wisher.username)
    items = Item.objects.filter(wisher=wisher, group=group)
    return render(request, "wishlist_app/group/user_wishlist.html", {
        "group": group,
        "wisher": wisher,
        "items": items
    })
