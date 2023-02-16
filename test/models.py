from django.db import models
from lesson.models import Lesson


class Test(models.Model):
    TEST_MODE_TYPES = [
        ('auto', 'Automated only problem testing'),
        ('manual', 'Manual only problem testing'),
        ('auto_and_manual', 'Manual then automated problem testing')
    ]

    name = models.CharField(max_length=500)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, related_name='tests', null=True)
    test_mode = models.CharField(max_length=30, choices=TEST_MODE_TYPES, default=TEST_MODE_TYPES[0][0])

    def __str__(self):
        return self.name
