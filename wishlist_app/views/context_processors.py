from wishlist_app.models import WishlistGroup


def global_context(request):
    print "adding context %s" % request
    if request.user.is_authenticated:
        return {
            "groups": WishlistGroup.get_groups_by_user(request.user)
        }

