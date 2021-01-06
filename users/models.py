from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class CourseAssign(models.Model):
    course = models.ForeignKey('course.Course', related_name='assigns', on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, related_name='assigns', on_delete=models.CASCADE, null=False)
    is_staff = models.BooleanField(default=False)


admin.site.register(User)
