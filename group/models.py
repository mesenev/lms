from django.db import models
from course.models import Course
from users.models import User
from django.contrib import admin


class Group(models.Model):
    course = models.ForeignKey(Course, related_name='source_for', on_delete=models.SET_NULL, null=True)
    group_schedule = models.JSONField(null=True, default=dict)
    points_for_passing = models.JSONField(null=True, default=dict)
    students = models.ManyToManyField(User, related_name='student_for', through='users.GroupAssignStudent')
    staff = models.ManyToManyField(User, related_name='staff_for', through='users.GroupAssignTeacher')


class GroupLink(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    link = models.CharField(max_length=500, null=True)
    usages = models.IntegerField(default=0)


admin.site.register(GroupLink)
admin.site.register(Group)
