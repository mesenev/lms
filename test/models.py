from django.db import models
from lesson.models import Lesson
import pydantic
from django_pydantic_field import SchemaField


class Answer(pydantic.BaseModel):
    text: str
    attachment_url: str = ''


class Question(pydantic.BaseModel):
    text: str
    correct_answers: list[Answer] = []
    all_answers: list[Answer] = []
    attachment_url: str = ''


class Test(models.Model):

    TEST_MODE_TYPES = [
        ('auto', 'Automated only testing'),
        ('manual', 'Manual only testing'),
        ('auto_and_manual', 'Manual then automated testing')
    ]
    question_list: list[Question] = SchemaField(default=[])
    name = models.CharField(max_length=500)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, related_name='tests', null=True)

    def __str__(self):
        return self.name
