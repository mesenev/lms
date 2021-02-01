from django.db import models

from users.models import User


class Course(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    author = models.ForeignKey(User, related_name='author_for', on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField(User, related_name='student_for', through='users.CourseAssignStudent')
    staff = models.ManyToManyField(User, related_name='staff_for', through='users.CourseAssignTeacher')
    cats_id = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class CourseSchedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_date = models.DateField(null=True)
    week_schedule = models.CharField(max_length=500, null=True)

class CourseLink(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    link = models.CharField(max_length=500, null=True)
    usages = models.IntegerField(default=0)