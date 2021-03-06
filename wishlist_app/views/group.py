from wishlist_app.forms.GroupForm import GroupForm
from wishlist_app.forms.RegistryForm import RegistryForm
from wishlist_app.forms.SecretSantaForm import SecretSantaFormSet
from django.shortcuts import render, get_object_or_404, redirect
from wishlist_app.models import GroupMember, WishlistGroup, Item, GroupItem, User, SecretSantaAssignment, RegistryAssignment
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.core.exceptions import PermissionDenied, FieldError, ValidationError
from django.http import HttpResponse, Http404, HttpResponseBadRequest


def get_home_template(group):
    if group.is_secret_santa():
        return "wishlist_app/group/secret_santa_home.html"
    elif group.is_registry():
        return "wishlist_app/group/registry_home.html"
    return "wishlist_app/group/group_home.html"


@login_required
@require_GET
def home(request, group_id):
    group = get_object_or_404(WishlistGroup, pk=group_id)
    if not group.contains_user(request.user):
        return redirect("wishlists")

    items = get_group_filtered_items(request.user, group)

    context = {
        "wishes": group.items.filter(wisher=request.user).order_by("name"),
        "gives": group.items.filter(giver=request.user).order_by("name"),
        "group": group,
        "members": group.members(),
        "assignment": group.get_assignment(request.user),
        "available_items": items["available"],
        "claimed_items": items["claimed"]
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
def clone(request, group_id):
    print "cloning group %s" % group_id
    group = get_object_or_404(WishlistGroup, pk=group_id)
    if request.POST['name'] is None:
       raise ValidationError("Name must be specified")
    name = request.POST['name']
    new_group = group.clone(name)
    return redirect("group_home", new_group.id)


@login_required
@require_POST
def delete(request, group_id):
    print "reading group %s" % group_id
    group = get_object_or_404(WishlistGroup, pk=group_id)
    if request.user != group.creator:
        print "user is not allowed to delete this group"
        raise PermissionDenied("Only the creator can delete a group")
    print "got group %s" % group
    try:
        group.remove_group()
    except Exception as e:
        print "couldn't delete group %s" % e
    print "Successfully deleted group"
    return redirect("wishlists")


@login_required
@require_GET
def user_wishlist(request, group_id, wisher_id):
    group = get_object_or_404(WishlistGroup, pk=group_id)
    wisher = get_object_or_404(User, pk=wisher_id)
    print "view user wishlist request: %s, user: %s" % (request.user, wisher)
    if request.user == wisher:
        return redirect("group_home", group.id)

    print "Wisher: %s: %s" % (wisher_id, wisher.username)

    items = get_group_filtered_items(request.user, group)

    return render(request, "wishlist_app/group/user_wishlist.html", {
        "group": group,
        "wisher": wisher,
        "available_items": items["available"].filter(wisher=wisher),
        "claimed_items": items["claimed"].filter(wisher=wisher),
        "assignment": group.get_assignment(request.user)
    })


@login_required
def assignments(request, group_id):
    group = get_object_or_404(WishlistGroup, pk=group_id)
    if not request.user == group.creator:
        raise PermissionDenied("Must be group creator to make assignments")
    if group.type == WishlistGroup.REGULAR:
        raise PermissionDenied("Group type doesn't support assignments")
    elif group.is_secret_santa():
        print "Secret Santa"
        # post
        if request.POST:
            return _post_secret_santa_assignments(request, group)
        # get
        else:
            return _get_secret_santa_assignments(request, group)
    elif group.is_registry():
        print "Registry/bday"
        # post
        if request.POST:
            return _post_registry_assignments(request, group)
        # get
        else:
            return _get_registry_assignments(request, group)
    # regular group doesn't have assignments
    return Http404


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


def get_group_filtered_items(user, group):
    assignment = group.get_assignment(user)
    available = group.items.filter(claimed=False).exclude(wisher=user)
    claimed = group.items.filter(claimed=True).exclude(wisher=user)

    # if group.is_secret_santa():
    #     if assignment is not None:
    #         available = available.filter(wisher=assignment.wisher)
    #         claimed = claimed.filter(giver=user)
    #     elif group.has_assignments():
    #         # if assignments have been made and someone doesn't have one, show them all wishes like a regular group
    #         pass
    #     else:
    #         # don't show items in ss when no assignments have been made yet
    #         available = available.none()
    #         claimed = claimed.none()

    return dict({
        "available": available,
        "claimed": claimed,
    })
