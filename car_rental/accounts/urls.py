from django.urls import path, reverse_lazy

from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path(
        "login/",
        LoginView.as_view(
            template_name="accounts/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),  
    path("profile/", views.profile, name="profile"),

    path(
        "password/",
        PasswordChangeView.as_view(
            template_name="accounts/password_change.html",
            # reverse_lazy because URLs aren't loaded yet when this line runs
            success_url=reverse_lazy("accounts:profile"),
        ),
        name="password_change",
    ),
    path("recover/", views.recover_password, name="recover_password"),
    path("logout/", LogoutView.as_view(), name="logout"),
]