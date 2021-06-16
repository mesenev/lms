from django.db import models
from django.contrib import admin
from course.models import Course
from lesson.models import Lesson
from users.models import User


class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, related_name='attendance', null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, related_name='attendance', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    be = models.BooleanField(default=False)


class CourseProgress(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, related_name='progress', null=True)
    progress = models.JSONField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    attendance = models.ManyToManyField(Attendance)

    class Meta:
        unique_together = ('course', 'user')


class LessonProgress(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, related_name='progress',blank=True, null=True)
    solved = models.JSONField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    attendance = models.ForeignKey(Attendance, on_delete=models.SET_NULL, related_name='lesson_attendance', null=True)

    class Meta:
        unique_together = ('lesson', 'user')


admin.site.register(CourseProgress)
admin.site.register(LessonProgress)
admin.site.register(Attendance)
