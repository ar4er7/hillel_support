from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        
        hashed_password = make_password(password)
        setattr(user, "password", hashed_password)
        # user.password = hashed_password

        user.save()
        # user.save(using=self._db) # if you have multiple databases
        
        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        pass