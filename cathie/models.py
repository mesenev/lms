from django.db import models

from users.models import User


class CatsUserLink(models.Model):
    pass
    # user = models.ForeignKey(User, related_name='cats_link', on_delete=models.CASCADE)
    # cats_id = models.IntegerField()
    # cats_token = models.CharField(max_length=50, null=True)


class CatsSubmit(models.Model):
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
        ('BA', 'Banned')
    ]
    problem = models.ForeignKey(CatsProblem, on_delete=models.CASCADE, null=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    source_text = models.TextField()
    status = models.CharField(max_length=2, choices=SUBMIT_STATUS)
