from wishlist_app.forms.GroupForm import GroupForm
from wishlist_app.forms.RegistryForm import RegistryForm
from wishlist_app.forms.SecretSantaForm import SecretSantaFormSet
from django.shortcuts import render, get_object_or_404, redirect
from wishlist_app.models import GroupMember, WishlistGroup, Item, User, SecretSantaAssignment, RegistryAssignment
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse


def get_home_template(group):
    if group.is_secret_santa():
        return "wishlist_app/group/secret_santa_home.html"
    elif group.is_registry():
        return "wishlist_app/group/registry_home.html"
    return "wishlist_app/group/group_home.html"


@login_required(login_url="login")
@require_GET
def home(request, group_id):
    group = get_object_or_404(WishlistGroup, pk=group_id)
    if not group.contains_user(request.user):
        return redirect("wishlists")

    assignment = group.get_assignment(request.user)

    available = Item.objects.filter(group=group, claimed=False).exclude(wisher=request.user)
    claimed = Item.objects.filter(group=group, claimed=True).exclude(wisher=request.user)

    if group.is_secret_santa():
        available = available.filter(wisher=assignment.wisher)
        claimed = claimed.filter(giver=request.user)

    context = {
        "wishes": Item.objects.filter(group=group, wisher=request.user).order_by("name"),
        "gives": Item.objects.filter(group=group, giver=request.user).order_by("name"),
        "group": group,
        "members": group.members(),
        "assignment": assignment,
        "available_items": available,
        "claimed_items": claimed
    }
    return render(request, get_home_template(group), context)


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
        f = GroupForm(request.POST, instance=group)
        if not f.is_valid():
            return render(request, 'wishlist_app/group/update_group.html', {'group_form': f, 'group': group})
        group = f.save()
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
    group.delete()
    print "Successfully deleted group"
    return redirect("wishlists")


@login_required
@require_GET
def user_wishlist(request, group_id, wisher_id):
    group = get_object_or_404(WishlistGroup, pk=group_id)
    wisher = get_object_or_404(User, pk=wisher_id)
    print "Wisher: %s: %s" % (wisher_id, wisher.username)

    assignment = group.get_assignment(request.user)

    available = Item.objects.filter(group=group, wisher=wisher, claimed=False)
    claimed = Item.objects.filter(group=group, wisher=wisher, claimed=True)

    if group.is_secret_santa():
        available = available.filter(wisher=assignment.wisher)
        claimed = claimed.filter(giver=request.user)

    return render(request, "wishlist_app/group/user_wishlist.html", {
        "group": group,
        "wisher": wisher,
        "available_items": available,
        "claimed_items": claimed,
        "assignment": group.get_assignment(request.user)
    })


@login_required
def assignments(request, group_id):
    group = get_object_or_404(WishlistGroup, pk=group_id)
    if not request.user == group.creator:
        raise PermissionDenied("Must be group creator to make assignments")
    if group.type == WishlistGroup.REGULAR:
        raise PermissionDenied("Group type doesn't support assignments")
    elif group.type == WishlistGroup.SECRET_SANTA:
        print "Secret Santa"
        # post
        if request.POST:
            return _post_secret_santa_assignments(request, group)
        # get
        else:
            return _get_secret_santa_assignments(request, group)
    elif group.type == WishlistGroup.REGISTRY:
        print "Registry/bday"
        # post
        if request.POST:
            return _post_registry_assignments(request, group)
        # get
        else:
            return _get_registry_assignments(request, group)

    return HttpResponse("assignments")


def _get_registry_assignments(request, group):
    try:
        a = RegistryAssignment.objects.get(group=group)
        f = RegistryForm(group, instance=a)
    except RegistryAssignment.DoesNotExist:
        f = RegistryForm(group)
    return render(request, "wishlist_app/group/registry_assignment.html", {
       "group": group,
       "form": f
    })


def _post_registry_assignments(request, group):
    try:
        a = RegistryAssignment.objects.get(group=group)
        f = RegistryForm(group, request.POST, instance=a)
        print "Updating an existing registry assignment: %s" % a
    except RegistryAssignment.DoesNotExist:
        print "first time creation of registry assignment for group"
        f = RegistryForm(group, request.POST)
    if not f.is_valid():
        return render(request, "wishlist_app/group/registry_assignment.html", {
           "group": group,
           "form": f
        })
    a = f.save(commit=False)
    a.group = group
    a = a.save()
    f.save_m2m()
    print "Saved registry user: %s" % a
    return redirect("group_home", group.id)


def _get_secret_santa_assignments(request, group):
    group.create_secret_santa_assignments()
    queryset = SecretSantaAssignment.objects.filter(group=group).order_by("wisher__username")
    print "ss assignments: %s" % queryset
    formset = SecretSantaFormSet(queryset=queryset)

    return render(request, "wishlist_app/group/ss_assignments.html", {
       "group": group,
       "formset": formset
    })


def _post_secret_santa_assignments(request, group):
    formset = SecretSantaFormSet(request.POST)
    if not formset.is_valid():
        return render(request, "wishlist_app/group/ss_assignments.html", {
           "group": group,
           "formset": formset
        })
    assignments = formset.save()
    return redirect("group_home", group.id)

