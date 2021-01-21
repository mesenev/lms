from django.db import models

from users.models import User


class CatsUserLink(models.Model):
    pass
    # user = models.ForeignKey(User, related_name='cats_link', on_delete=models.CASCADE)
    # cats_id = models.IntegerField()
    # cats_token = models.CharField(max_length=50, null=True)
