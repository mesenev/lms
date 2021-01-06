from django.db import models

from lesson.models import Lesson
from users.models import User


class Problem(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, related_name='problems', null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=500)
    description = models.TextField()


class Submit(models.Model):
    SUBMIT_STATUS = [('WA', 'Wrong answer'), ('OK', 'OK'), ('NP', 'NP'), ]
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    content = models.TextField()
    status = models.CharField(max_length=2, choices=SUBMIT_STATUS)
