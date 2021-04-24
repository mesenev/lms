from django.db import models
from course.models import Course
from lesson.models import Lesson
from users.models import User


class CourseProgress(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, related_name='progress', null=True)
    lessons = models.JSONField(null=True)
    attendance = models.JSONField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('course', 'user')


class LessonProgress(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, related_name='progress', null=True)
    solved = models.JSONField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('lesson', 'user')
