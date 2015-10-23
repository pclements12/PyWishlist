from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_http_methods


@require_http_methods(['GET', 'POST'])
def request_login(request):
    if request.POST:
        print "attempting login"
        form = AuthenticationForm(data=request.POST)
        if not form.is_valid():
            print "auth form is not valid"
            form.add_error(None, "Login failed")
            return render(request, "wishlist_app/login.html", {"login_form": form})
        "auth form is valid"
        username = request.POST['username']
        password = request.POST['password']
        print "authenticating %s" % username
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("wishlists")
    else:
        form = AuthenticationForm()
        return render(request, "wishlist_app/login.html", {"login_form": form})


@login_required
@require_GET
def do_logout(request):
    logout(request)
    return redirect("wishlists")


@login_required
@require_GET
def wishlists(request):
    return render(request, "wishlist_app/wishlists.html")


