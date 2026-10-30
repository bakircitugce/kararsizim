from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import LoginForm, SignupForm


def _safe_next_url(request, fallback):
    next_url = request.POST.get("next") or request.GET.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return fallback


def _guest_only(view):
    return user_passes_test(
        lambda user: not user.is_authenticated,
        login_url="/",
        redirect_field_name=None,
    )(view)


@_guest_only
def signup(request):
    next_url = _safe_next_url(request, reverse("home"))
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form, "next": next_url})


@_guest_only
def login_view(request):
    next_url = _safe_next_url(request, reverse("home"))
    if request.method == "POST":
        form = LoginForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(next_url)
    else:
        form = LoginForm(request)
    return render(request, "accounts/login.html", {"form": form, "next": next_url})


def logout_view(request):
    if request.method != "POST":
        return redirect("home")
    logout(request)
    messages.success(request, "Çıkış yaptın.")
    return redirect("home")
