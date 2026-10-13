from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import RegisterForm


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