from django.db import models

from course.models import Course
from users.models import User


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, related_name='lessons', null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=500)
    description = models.TextField()
    deadline = models.DateField(blank=True, null=True)


class LessonContent(models.Model):
    CONTENT_TYPE = [
        ('video', 'Video'),
        ('text', 'Text'),
        ('url', 'Url'),
    ]

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    content_type = models.CharField(max_length=5, choices=CONTENT_TYPE)
    content = models.TextField()
