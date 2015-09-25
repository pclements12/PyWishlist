from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from wishlist_app.models import WishlistGroup
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def request_login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("wishlists")
        else:
            return HttpResponse('Unauthorized', status=401)
    else:
        form = AuthenticationForm()
        return render(request, "wishlist_app/login.html", {"login_form": form})


def do_logout(request):
    logout(request)
    return redirect("wishlists")

@login_required(login_url="login")
def wishlists(request):
    groups = WishlistGroup.get_groups_by_user(request.user)
    print groups
    context = {
        "wishlists": groups
    }
    return render(request, "wishlist_app/wishlists.html", context)


