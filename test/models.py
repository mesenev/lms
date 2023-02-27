from django.db import models
from lesson.models import Lesson
import pydantic
from django_pydantic_field import SchemaField


class Answer(pydantic.BaseModel):
    text: str
    attachment_url: str = ''


class Question(pydantic.BaseModel):
    test: int
    text: str
    description: str
    correct_answers: list[Answer] = []
    all_answers: list[Answer] = []
    answer_type: str
    attachment_url: str = ''
    points: int


class Test(models.Model):
    TEST_MODE_TYPES = [
        ('auto', 'Automated only testing'),
        ('manual', 'Manual only testing'),
        ('auto_and_manual', 'Manual then automated testing')
    ]
    description = models.TextField(default='')
    questions: list[Question] = SchemaField(default=[])
    points = models.IntegerField()
    name = models.CharField(max_length=500)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, related_name='tests', null=True)
    is_hidden = models.BooleanField(default=True)
    test_mode = models.CharField(max_length=30, choices=TEST_MODE_TYPES, default=TEST_MODE_TYPES[0][0])

    def __str__(self):
        return self.name
