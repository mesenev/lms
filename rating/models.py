from django.db import models
from django.contrib import admin
from course.models import Course
from lesson.models import Lesson
from users.models import User


class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='attendance')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    be = models.BooleanField(default=False)


class CourseProgress(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progress')
    progress = models.JSONField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attendance = models.ManyToManyField(Attendance)

    class Meta:
        unique_together = ('course', 'user')


class LessonProgress(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    solved = models.JSONField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='lesson_attendance')

    class Meta:
        unique_together = ('lesson', 'user')


admin.site.register(CourseProgress)
admin.site.register(LessonProgress)
admin.site.register(Attendance)
