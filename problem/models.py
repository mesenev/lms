from django.db import models

from lesson.models import Lesson
from users.models import User


class Problem(models.Model):
    PROBLEM_TYPES = [('CW', 'classwork'), ('HW', 'homework')]
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, related_name='problems', null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=500)
    description = models.TextField()
    manual = models.BooleanField(default=False)
    type = models.CharField(max_length=2, choices=PROBLEM_TYPES, default=PROBLEM_TYPES[0][0])
    language = models.CharField(max_length=100, null=True, blank=True)
    cats_id = models.IntegerField(null=True)
    cats_material_url = models.URLField(null=False)


class Submit(models.Model):
    SUBMIT_STATUS = [
        ('WA', 'Wrong answer'),
        ('OK', 'OK'),
        ('NP', 'NP'),
        ('RJ', 'Rejected'),
        ('CE', 'Compilation error'),
        ('LI', 'Linter error'),
        ('RE', 'Run-time error'),
        ('PE', 'Presentation error'),
        ('TL', 'Time limit exceeded'),
        ('IL', 'Idleness limit exceeded'),
        ('ML', 'Memory limit exceeded'),
        ('WL', 'Write limit exceeded'),
        ('SV', 'Security violation'),
        ('IS', 'Ignored submit'),
        ('AW', 'Awaiting manual verification'),
        ('MR', 'Rejected by manual verification'),
        ('BA', 'Banned'),
    ]
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    content = models.TextField()
    cats_request_id = models.IntegerField(null=True)
    status = models.CharField(max_length=2, choices=SUBMIT_STATUS, default='NP')

    def __str__(self):
        return self.status
