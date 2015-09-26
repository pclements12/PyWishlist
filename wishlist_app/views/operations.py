from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from wishlist_app.models import WishlistGroup
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def request_login(request):
    if request.POST:
        print "attempting login"
        username = request.POST['username']
        password = request.POST['password']
        print "authenticating %s" % username
        user = authenticate(username=username, password=password)
        if user is not None:
            print "processing logging in"
            login(request, user)
            return redirect("wishlists")
        else:
            print "couldn't authenticate"
            return HttpResponse('Unauthorized', status=401)
    else:
        form = AuthenticationForm()
        return render(request, "wishlist_app/login.html", {"login_form": form})


def do_logout(request):
    logout(request)
    return redirect("wishlists")


@login_required
def wishlists(request):
    groups = WishlistGroup.get_groups_by_user(request.user)
    print groups
    context = {
        "wishlists": groups
    }
    return render(request, "wishlist_app/wishlists.html", context)


