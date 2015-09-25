from wishlist_app.forms.ItemForm import ItemForm
from django.shortcuts import render, get_object_or_404, redirect
from wishlist_app.models import WishlistGroup, Item
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.core.exceptions import PermissionDenied
import datetime


@login_required
@require_http_methods(["GET", "POST"])
def create(request, group_id):
    group = get_object_or_404(WishlistGroup, pk=group_id)
    print "Group: %s" % group
    print "Wisher: %s" % request.user
    if request.POST:
        print "posted values %s" % request.POST
        item_form = ItemForm(request.POST)
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

# >> user = User.objects.create()
# >> user.username = "patrick"
# >> user.save()

# >> group = WishlistGroup.objects.create()
# >> group.name = "Patrick's Group"
# >> group.save()

# >> item = Item.objects.create()
# >> item.name = "Soccer ball"
# >> item.description = "size 5"
# >> item.link = "http://lmgtfy.com?q=size+5+soccer+ball"
# >> item.wisher = user
# >> item.group = group
# >> item.save()


def do_read(request, item_id):
    item = Item.objects.get(id=item_id)
    # pass request, template name, and template context to the render method
    return render(request, "wishlist_app/item/test.html", {"item": item})

# handles both GET to receive the form and POST to update the model
@login_required
def do_update(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    print "Update item: %s" % item
    if request.POST:
        print "posted values %s" % request.POST
        item.name = request.POST['name']
        item.description = request.POST['description']
        item.link = request.POST['link']
        item.quantity = request.POST['quantity']
        item.save()
        print "update item %s" % item
        return redirect("do_item_read", item.id)
    else:
        # on GET, serve up our Item Form
        item_form = ItemForm(instance=item)
        return render(request, 'wishlist_app/item/update_item.html',
                        {'item_form': item_form, 'item': item})


@login_required
@require_GET
def read(request, item_id):
    print "looking for item %s" % item_id
    item = get_object_or_404(Item, pk=item_id)
    print "got item %s" % item
    return render(request, "wishlist_app/item/item.html", {"item": item})


@login_required
@require_http_methods(["GET", "POST"])
def update(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.user != item.wisher:
        print "user is not allowed to edit this item"
        raise PermissionDenied("Only the wisher can edit an item")

    print "Update item: %s" % item
    if request.POST:
        print "posted values %s" % request.POST
        item.name = request.POST['name']
        item.description = request.POST['description']
        item.link = request.POST['link']
        item.quantity = request.POST['quantity']
        item.save()
        print "update item %s" % item
        return redirect("group_home", item.group.id)
    else:
        item_form = ItemForm(instance=item)
        return render(request, 'wishlist_app/item/update_item.html', {'item_form': item_form, 'item': item})


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
@require_GET
def claim(request, item_id):
    print "claiming item %s" % item_id
    item = get_object_or_404(Item, pk=item_id)
    if item.giver is not None:
        raise PermissionDenied("Item has already been claimed")
    if request.user == item.wisher:
        raise PermissionDenied("User's can't claim their own items")
    print "got item %s" % item
    print "updating item %s for claim by %s" % (item, request.user)
    item.claim(request.user)
    print "item successfully claimed"
    return render(request, 'wishlist_app/item/item.html', {"item": item})


@login_required
@require_GET
def unclaim(request, item_id):
    print "unclaiming item %s" % item_id
    item = get_object_or_404(Item, pk=item_id)
    if item.giver != request.user:
        raise PermissionDenied("Item must be claimed by user to be unclaimed")
    if request.user == item.wisher:
        raise PermissionDenied("User's can't claim their own items")
    print "got item %s" % item
    print "updating item %s for unclaim by %s" % (item, request.user)
    item.unclaim()
    print "item successfully claimed"
    return render(request, 'wishlist_app/item/item.html', {"item": item})
