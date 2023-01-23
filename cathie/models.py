from django.db import models
from django.contrib import admin
from django.utils import timezone

from users.models import User


class CatsUserLink(models.Model):
    pass
    # user = models.ForeignKey(User, related_name='cats_link', on_delete=models.CASCADE)
    # cats_id = models.IntegerField()
    # cats_token = models.CharField(max_length=50, null=True)


class CatsAccount(models.Model):
    user = models.OneToOneField(User, related_name='cats_account', on_delete=models.CASCADE)
    username = models.CharField(max_length=50, null=False)
    cats_user_id = models.IntegerField(null=False)
    last_check = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'lms: {self.user} - cats: {self.username}'


admin.site.register(CatsAccount)
