from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager

# class User(models.Model):

#     password = models.CharField(max_length=100)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # password field is already provided by AbstractBaseUser
    # last_login field is already provided by AbstractBaseUser

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # is_superuser field is already provided by PermissionsMixin
    date_joined = models.DateTimeField(default=timezone.now)

    role = models.CharField(max_length=20)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_full_name()
        else:
            return self.email
