from django.contrib import admin
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


admin.site.register(User)
