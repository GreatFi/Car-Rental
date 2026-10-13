from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Manager for a user model that logs in with email instead of username."""

    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError("Email is required")
        # lowercase the whole address so Ola@x.com and ola@x.com are one account
        email = email.strip().lower()
        user = self.model(email=email, **extra)
        user.set_password(password)  # hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra):
        # createsuperuser calls this, so make sure admin flags are on
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra)


class User(AbstractUser):
    username = None  # remove the username field entirely
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]  # asked for by createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.email   