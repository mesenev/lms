from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class CourseAssignStudent(models.Model):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, related_name='assigns', on_delete=models.CASCADE, null=False)


class CourseAssignTeacher(models.Model):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)


admin.site.register(User)
