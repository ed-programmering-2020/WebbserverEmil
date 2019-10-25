from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager


class User(AbstractBaseUser):
    USERNAME_FIELD = "username"
    objects = UserManager()

    username = models.CharField("username", max_length=32, unique=True, db_index=True)
    email = models.EmailField("email", unique=True)
    joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __unicode__(self):
        return self.username
