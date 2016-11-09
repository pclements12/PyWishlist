from wishlist_app.forms.ItemForm import ItemForm
from wishlist_app.forms.CommentForm import CommentForm
from django.shortcuts import render, get_object_or_404, redirect
from wishlist_app.models import WishlistGroup, Item, Comment, ItemComment, GroupItem
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.core.exceptions import PermissionDenied, ValidationError
from wishlist_app.forms.GroupItemsForm import GroupItemsForm


@login_required
@require_http_methods(["GET", "POST"])
def list(request, group_id):
    group = get_object_or_404(WishlistGroup, pk=group_id)
    if request.POST:
        form = GroupItemsForm(request.POST, instance=group, user=request.user)
        if form.is_valid():
            group_items = form.save()
            return redirect("group_home", group.id)
    else:
        form = GroupItemsForm(instance=group, user=request.user)
    return render(request, "wishlist_app/group/group_list.html", {
        "form": form,
        "group": group
    })


# creating an item within a group automatically adds the group_item associating them
@login_required
@require_http_methods(["GET", "POST"])
def create(request, group_id):
    group = get_object_or_404(WishlistGroup, pk=group_id)
    print "Wisher: %s" % request.user
    if request.POST:
        print "posted values %s" % request.POST
        item_form = ItemForm(request.POST, user=request.user)
        print "load item form %s" % item_form
        if not item_form.is_valid():
            print "form is invalid"
            return render(request, 'wishlist_app/item/new_item.html',
                          {'item_form': item_form,
                           "group": group})
        print "form is valid"
        item = item_form.save(commit=False)
        print "create uncommited item"
        item.wisher = request.user
        item.save()
        print "item saved, creating group item relations"
        item_form.save_m2m()
        print "created a new item %s" % item
        print "redirecting to the group home page"
        return redirect("group_home", group.id)
    else:
        item_form = ItemForm(group=group, user=request.user)
        return render(request, 'wishlist_app/item/new_item.html',
                      {'item_form': item_form,
                       "group": group})


@login_required
@require_GET
def read(request, group_id, item_id):
    print "looking for item %s" % item_id
    item = get_object_or_404(Item, pk=item_id)
    group = get_object_or_404(WishlistGroup, pk=group_id)
    group_item = GroupItem.objects.get(item=item, group=group)
    print "got item %s" % item
    context = {
        "group": group,
        "item": item,
        "comments": group_item.comments.order_by('created'),
        "comment_form": CommentForm(),
        "action_url": "item_comment",
        "action_id": item.id
    }
    return render(request, "wishlist_app/group_item/item.html", context)


@login_required
@require_POST
def remove_item(request, group_item_id):
    print "remove group item %s" % group_item_id
    group_item = get_object_or_404(Item, pk=group_item_id)
    if request.user != group_item.item.wisher:
        print "user is not allowed to delete this item"
        raise PermissionDenied("Only the wisher can delete an item")
    print "got item %s" % group_item.item
    group_id = group_item.group.id
    group_item.delete()
    return redirect("group_home", group_id)


@login_required
@require_POST
def claim(request, group_id, item_id):
    print "claiming item %s" % item_id
    item = get_object_or_404(Item, pk=item_id)
    group = get_object_or_404(WishlistGroup, pk=group_id)
    item.check_claim(request.user)
    print "got item %s" % item
    print "updating item %s for claim by %s" % (item, request.user)
    item.claim(request.user)
    print "item successfully claimed"

    # group id is used for the user wishlist links in the row
    return render(request, 'wishlist_app/item/item_row.html', {'item': item, 'group': group})


@login_required
@require_POST
def unclaim(request, group_id, item_id):
    print "unclaiming item %s" % item_id
    item = get_object_or_404(Item, pk=item_id)
    group = get_object_or_404(WishlistGroup, pk=group_id)
    if item.giver != request.user:
        raise PermissionDenied("Item must be claimed by user to be unclaimed")
    if request.user == item.wisher:
        raise PermissionDenied("Users can't unclaim their own items")
    print "got item %s" % item
    print "updating item %s for unclaim by %s" % (item, request.user)
    item.unclaim()
    print "item successfully unclaimed"
    # group id is used for the user wishlist links in the row?
    return render(request, 'wishlist_app/item/item_row.html', {'item': item, 'group': group})


@login_required
@require_POST
def comment(request, group_id, item_id):
    item = get_object_or_404(Item, pk=item_id)
    group = get_object_or_404(WishlistGroup, pk=group_id)
    group_item = GroupItem.objects.get(item=item, group=group)

    print "adding a coment to %s" % item
    print "posted values %s" % request.POST
    form = CommentForm(request.POST)
    if not form.is_valid():
        print "comment form is invalid"
        return render(request, "wishlist_app/item/item.html", {
            "item": item,
            "comments": item.comments.order_by('created'),
            "comment_form": form
        })
    print "saving comment"
    c = form.save(commit=False)
    c.commenter = request.user
    # TODO refactor this to be more DRY
    if c.hide_from_wisher and c.commenter == item.wisher:
        form.add_error("hide_from_wisher", ValidationError("Can't hide comments from yourself"))
        return render(request, "wishlist_app/item/item.html", {
            "item": item,
            "comments": group_item.comments.order_by('created'),
            "comment_form": form
        })
    c.save()
    ic = ItemComment(group_item=group_item, comment=c)
    ic.save()
    print "saved comment %s" % c
    return redirect("group_item_read", group.id,  item.id)


@login_required
@require_http_methods(["GET", "POST"])
def edit_comment(request, comment_id):
    print "Request to edit comment: %s" % comment_id
    c = get_object_or_404(Comment, pk=comment_id)
    print "Got Comment %s" % c
    ic = get_object_or_404(ItemComment, comment=c)
    print "Got item-comment"
    item = ic.group_item.item
    print "Got item %s" % item
    if not request.user == c.commenter:
        raise PermissionDenied("Can't edit a comment you didn't write")
    if request.POST:
        print "post request to edit comment, bound to %s" % c
        form = CommentForm(request.POST, instance=c)
        print "bound form: %s" % form
        if not form.is_valid():
            print "comment form is invalid"
            return render(request, "wishlist_app/item/item.html", {
                "item": item,
                "comments": item.comments.order_by('created'),
                "comment_form": form
            })
        else:
            print "comment form valid"
            c = form.save()
            print "comment update saved: %s" % c
            return redirect("group_item_read", ic.group_item.group.id, item.id)
    else:
        print "request for a comment form bound to %s" % c
        form = CommentForm(instance=c)
        print "Form is type: %s" % type(form)
        print "Item is type: %s" % type(item)
        return render(request, "wishlist_app/comment/update_comment_form.html", {
            "item": item,
            "comment": c,
            "comment_form": form
        })
