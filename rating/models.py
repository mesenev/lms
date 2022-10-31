from django.db import models
from django.contrib import admin
from course.models import Course
from lesson.models import Lesson
from users.models import User


class CourseProgress(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progress')
    progress = models.JSONField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course', 'user')


class LessonProgress(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    solved = models.JSONField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attendance = models.BooleanField(default=False)

    class Meta:
        unique_together = ('lesson', 'user')


admin.site.register(CourseProgress)
admin.site.register(LessonProgress)
