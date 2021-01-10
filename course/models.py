from django.db import models

from users.models import User


class Course(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class CourseSchedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_date = models.DateField(null=True)
    week_schedule = models.CharField(max_length=500, null=True)
