from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    middle_name = models.CharField(max_length=50, blank=True)
    avatar_url = models.ImageField(upload_to='avatars', null=True, blank=True)

    def get_avatar(self):
        if not self.avatar_url:
            return '/media/user.png'
        return self.avatar_url.url


class CourseAssignStudent(models.Model):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, related_name='assigns', on_delete=models.CASCADE, null=False)


class CourseAssignTeacher(models.Model):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)


admin.site.register(User)
