from django.contrib import admin
from django.db import models
from lesson.models import Lesson
from users.models import User


class ProblemManager(models.Manager):
    def get_queryset(self):
        problems = super().get_queryset().select_related('lesson__course')
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
    PROBLEM_TYPES = [('CW', 'classwork'), ('HW', 'homework'), ('EX', 'extratasks')]
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, related_name='problems', null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authored_problems', null=True)
    name = models.CharField(max_length=500)
    description = models.TextField()
    manual = models.BooleanField(default=False)
    type = models.CharField(max_length=2, choices=PROBLEM_TYPES, default=PROBLEM_TYPES[0][0])
    language = models.CharField(max_length=100, null=True, blank=True)
    cats_id = models.IntegerField(null=True)
    cats_material_url = models.URLField(null=False)
    students = models.ManyToManyField(
        through='problem.Submit',
        through_fields=('problem', 'student'),
        related_name='problems_with_submits',
        to=User
    )
    de_options = models.CharField(max_length=512, blank=True, default='')
    test_mod = models.CharField(max_length=512, blank=True, default='')
    objects = ProblemManager()


class ProblemStats(models.Model):
    problem = models.OneToOneField(Problem, on_delete=models.CASCADE)
    green = models.IntegerField()
    yellow = models.IntegerField()
    red = models.IntegerField()


class Submit(models.Model):
    DEFAULT_STATUS = 'NP'
    WRONG_ANSWER = 'WA'
    AWAITING_MANUAL = 'AW'
    OK = 'OK'
    SUBMIT_STATUS = [
        (WRONG_ANSWER, 'Wrong answer'),
        (OK, 'OK'),
        (DEFAULT_STATUS, 'NP'),
        (AWAITING_MANUAL, 'Awaiting manual verification'),
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
        ('MR', 'Rejected by manual verification'),
        ('BA', 'Banned'),
    ]
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='submits', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, related_name='updated_submits', on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submits', null=False)
    content = models.TextField()
    status = models.CharField(max_length=2, choices=SUBMIT_STATUS, default='NP')
    de_id = models.CharField(max_length=5)

    def __str__(self):
        return f'ID{self.id} - {self.status}'

    class Meta:
        ordering = ['id']


class CatsSubmit(models.Model):
    submit = models.ForeignKey(Submit, related_name='cats_submit', on_delete=models.DO_NOTHING, null=True)
    data = models.JSONField(null=False)
    id_to_check = models.IntegerField(null=True, default=None)
    is_sent = models.BooleanField(default=False, null=False)
    sending_result = models.JSONField(null=True)
    testing_result = models.JSONField(null=True)
    is_error = models.BooleanField(default=False, null=False)

    def __str__(self):
        return f'CID{self.submit.id} - ({"sent" if self.is_sent else "nsent"})'


class LogEvent(models.Model):
    TYPE_MESSAGE = 'message'
    TYPE_CATS_ANSWER = 'cats_answer'
    TYPE_STATUS_CHANGE = 'status_change'
    TYPE_SUBMIT = 'submit'
    TYPE_CATS_SUBMIT = 'cats_submit'
    TYPE_CATS_ERROR = 'cats_error'
    LOG_EVENT_TYPES = [
        (TYPE_SUBMIT, 'Submit created'),
        (TYPE_MESSAGE, 'Message to display'),
        (TYPE_STATUS_CHANGE, 'Submit status changed to'),
        (TYPE_CATS_ANSWER, 'Check answer from cats'),
        (TYPE_CATS_SUBMIT, 'Cats submit created'),
        (TYPE_CATS_ERROR, 'Cats error type'),
    ]
    type = models.CharField(max_length=16, choices=LOG_EVENT_TYPES)
    problem = models.ForeignKey(Problem, related_name='log_events', on_delete=models.CASCADE, null=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='log_events', null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_log_events', null=True)
    submit = models.ForeignKey(Submit, on_delete=models.CASCADE, related_name='log_events', null=True)
    data = models.JSONField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at', 'id')


admin.site.register(Problem)
admin.site.register(Submit)
admin.site.register(CatsSubmit)
admin.site.register(LogEvent)
