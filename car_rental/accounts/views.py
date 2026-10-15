from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.db.models import Count, Q

from .forms import PasswordRecoveryForm, ProfileForm, RegisterForm


def register(request):
    # logged-in users have no reason to see the signup page
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()    # hashes the password through UserCreationForm
            login(request, user)  # log in straight away
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = RegisterForm()     # empty form on GET

    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated.")
        return redirect("accounts:profile")

    bookings = request.user.bookings
    # one query gives all three counts, instead of three separate ones
    stats = bookings.aggregate(
        total=Count("id"),
        pending=Count("id", filter=Q(status="pending")),
        confirmed=Count("id", filter=Q(status="confirmed")),
    )
    pending_bookings = bookings.filter(status="pending").select_related("vehicle__brand")

    return render(request, "accounts/profile.html", {
        "form": form,
        "stats": stats,
        "pending_bookings": pending_bookings,
    })

def recover_password(request):
    # logged-in users have change password instead
    if request.user.is_authenticated:
        return redirect("accounts:profile")

    form = PasswordRecoveryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Password updated. You can log in now.")
        return redirect("accounts:login")  # no auto-login: they prove it by logging in
    return render(request, "accounts/recover_password.html", {"form": form})