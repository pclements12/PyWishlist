from wishlist_app.forms.ItemForm import ItemForm
from wishlist_app.forms.CommentForm import CommentForm
from django.shortcuts import render, get_object_or_404, redirect
from wishlist_app.models import WishlistGroup, Item, Comment, ItemComment
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.core.exceptions import PermissionDenied, ValidationError


@login_required
@require_http_methods(["GET", "POST"])
def create(request, group_id):
    group = get_object_or_404(WishlistGroup, pk=group_id)
    print "Group: %s" % group
    print "Wisher: %s" % request.user
    if request.POST:
        print "posted values %s" % request.POST
        item_form = ItemForm(request.POST)
        if not item_form.is_valid():
             return render(request, 'wishlist_app/item/new_item.html',
                      {'item_form': item_form,
                       "group": group})
        item = item_form.save(commit=False)
        item.group = group
        item.wisher = request.user
        item.save()
        print "creating a new item %s" % item
        return redirect("group_home", item.group.id)
    else:
        item_form = ItemForm()
        return render(request, 'wishlist_app/item/new_item.html',
                      {'item_form': item_form,
                       "group": group})


@login_required
@require_GET
def read(request, item_id):
    print "looking for item %s" % item_id
    item = get_object_or_404(Item, pk=item_id)
    print "got item %s" % item
    context = {
        "item": item,
        "comments": item.comments.order_by('created'),
        "comment_form": CommentForm(),
        "action_url": "item_comment",
        "action_id": item.id,
        "assignment": item.group.get_assignment(request.user)
    }
    return render(request, "wishlist_app/item/item.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def update(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    assignment = item.group.get_assignment(request.user)
    if request.user != item.wisher:
        print "user is not allowed to edit this item"
        raise PermissionDenied("Only the wisher can edit an item")

    print "Update item: %s" % item
    if request.POST:
        print "posted values %s" % request.POST
        item_form = ItemForm(request.POST, instance=item)
        if not item_form.is_valid():
            return render(request, 'wishlist_app/item/update_item.html',
                          {'item_form': item_form,
                           'item': item,
                           'assignment': assignment})
        u_item = item_form.save(commit=False)
        if int(u_item.quantity) < 1:
            print "item quantity less than 1, defaulting to 1"
            u_item.quantity = 1
        saved_item = item_form.save()
        item_form.save_m2m()
        print "update item %s" % saved_item
        return redirect("item_read", item.id)
    else:
        item_form = ItemForm(instance=item)
        return render(request, 'wishlist_app/item/update_item.html',
                      {'item_form': item_form,
                       'item': item,
                       'assignment': assignment})


@login_required
@require_POST
def delete(request, item_id):
    print "reading item %s" % item_id
    item = get_object_or_404(Item, pk=item_id)
    if request.user != item.wisher:
        print "user is not allowed to delete this item"
        raise PermissionDenied("Only the wisher can delete an item")
    print "got item %s" % item
    group_id = item.group.id
    item.delete()
    return redirect("group_home", group_id)


@login_required
@require_POST
def claim(request, item_id):
    print "claiming item %s" % item_id
    item = get_object_or_404(Item, pk=item_id)
    item.check_claim(request.user)
    print "got item %s" % item
    print "updating item %s for claim by %s" % (item, request.user)
    item.claim(request.user)
    print "item successfully claimed"
    return render(request, 'wishlist_app/item/item_row.html', {'item': item, 'group': item.group})


@login_required
@require_POST
def unclaim(request, item_id):
    print "unclaiming item %s" % item_id
    item = get_object_or_404(Item, pk=item_id)
    if item.giver != request.user:
        raise PermissionDenied("Item must be claimed by user to be unclaimed")
    if request.user == item.wisher:
        raise PermissionDenied("Users can't unclaim their own items")
    print "got item %s" % item
    print "updating item %s for unclaim by %s" % (item, request.user)
    item.unclaim()
    print "item successfully claimed"
    return render(request, 'wishlist_app/item/item_row.html', {'item': item, 'group': item.group})


@login_required
@require_POST
def comment(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    print "adding a coment to %s" % item
    print "posted values %s" % request.POST
    form = CommentForm(request.POST)
    if not form.is_valid():
        print "comment form is invalid"
        return render(request, "wishlist_app/item/item.html", {
            "item": item,
            "comments": item.comments.order_by('created'),
            "comment_form": form,
            "assignment": item.group.get_assignment(request.user)
        })
    print "saving comment"
    c = form.save(commit=False)
    c.commenter = request.user
    # TODO refactor this to be more DRY
    if c.hide_from_wisher and c.commenter == item.wisher:
        form.add_error("hide_from_wisher", ValidationError("Can't hide comments from yourself"))
        return render(request, "wishlist_app/item/item.html", {
            "item": item,
            "comments": item.comments.order_by('created'),
            "comment_form": form,
            "assignment": item.group.get_assignment(request.user)
        })
    c.save()
    ic = ItemComment(item=item, comment=c)
    ic.save()
    print "saved comment %s" % c
    return redirect("item_read", item.id)


@login_required
@require_http_methods(["GET", "POST"])
def edit_comment(request, comment_id):
    print "Request to edit comment: %s" % comment_id
    c = get_object_or_404(Comment, pk=comment_id)
    print "Got Comment %s" % c
    ic = get_object_or_404(ItemComment, comment=c)
    print "Got item-comment"
    item = ic.item
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
                "comment_form": form,
                "assignment": item.group.get_assignment(request.user)
            })
        else:
            print "comment form valid"
            c = form.save()
            print "comment update saved: %s" % c
            return redirect("item_read", item.id)
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

