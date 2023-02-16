from django.db import models
from lesson.models import Lesson


class Test(models.Model):
    name = models.CharField(max_length=500)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, related_name='tests', null=True)

    def __str__(self):
        return self.name