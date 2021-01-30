from django.db import models

from lesson.models import Lesson
from users.models import User


class ProblemManager(models.Manager):
    def get_queryset(self):
        problems = super().get_queryset()
        submit_query = Submit.objects.annotate(
            ordering=models.Case(
                models.When(status="OK", then=models.Value(0)),
                models.When(status="AW", then=models.Value(1)),
                default=models.Value(2),
                output_field=models.IntegerField()
            )
        ).order_by('ordering', '-id').filter(problem__in=models.Subquery(problems.values('id')))

        user_query = User.objects.prefetch_related(
            models.Prefetch(lookup='submits', queryset=submit_query)
        )
        problems = super().get_queryset().prefetch_related(
            models.Prefetch(lookup='students', queryset=user_query.distinct())
        ).prefetch_related('submits').select_related('author')
        return problems


class Problem(models.Model):
    PROBLEM_TYPES = [('CW', 'classwork'), ('HW', 'homework')]
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, related_name='problems', null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authored_problems', null=True)
    name = models.CharField(max_length=500)
    description = models.TextField()
    manual = models.BooleanField(default=False)
    type = models.CharField(max_length=2, choices=PROBLEM_TYPES, default=PROBLEM_TYPES[0][0])
    language = models.CharField(max_length=100, null=True, blank=True)
    cats_id = models.IntegerField(null=True)
    cats_material_url = models.URLField(null=False)
    students = models.ManyToManyField(through='problem.Submit', related_name='problems_with_submits', to=User)
    objects = ProblemManager()


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
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='submits', null=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submits', null=False)
    content = models.TextField()
    cats_request_id = models.IntegerField(null=True)
    status = models.CharField(max_length=2, choices=SUBMIT_STATUS, default='NP')

    def __str__(self):
        return self.status
