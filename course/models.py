from django.contrib import admin
from django.db import models

from users.models import User


class Course(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    author = models.ForeignKey(User, related_name='author_for', on_delete=models.SET_NULL, null=True)
    cats_id = models.IntegerField(null=True, help_text='contest_id from cats (cid)')
    de_options = models.CharField(max_length=512, blank=True, default='')

    def __str__(self):
        return self.name


class CourseSchedule(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='schedule')
    start_date = models.DateField(null=True, )
    week_schedule = models.JSONField(null=True, default=dict)
    lessons = models.JSONField(null=True, default=dict)


class CourseLink(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    link = models.CharField(max_length=500, null=True)
    usages = models.IntegerField(default=0)


admin.site.register(Course)
admin.site.register(CourseSchedule)
admin.site.register(CourseLink)
