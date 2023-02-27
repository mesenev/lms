from django.db import models
from django.contrib import admin
from lesson.models import Lesson
import pydantic
from django_pydantic_field import SchemaField
from users.models import User
from pydantic import validate_arguments


class Answer(pydantic.BaseModel):
    text: str
    file_url: str


class Question(pydantic.BaseModel):
    text: str
    description: str = ''
    correct_answers: list[str] = []
    all_answers: list[str] = []
    answer_type: str
    attachment_url: str = ''
    points: int


class Test(models.Model):
    TEST_MODE_TYPES = [
        ('auto', 'Automated only testing'),
        ('manual', 'Manual only testing'),
        ('auto_and_manual', 'Manual then automated testing')
    ]
    name = models.CharField(max_length=500)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, related_name='tests', null=True)
    description = models.TextField(default='')
    questions = models.JSONField()
    points = models.IntegerField()
    is_hidden = models.BooleanField(default=True)
    test_mode = models.CharField(max_length=30, choices=TEST_MODE_TYPES, default=TEST_MODE_TYPES[0][0])

    @classmethod
    @validate_arguments
    def create(cls, name, lesson, description, questions: list[Question], points, is_hidden, test_mode):
        test = cls(name, lesson, description, questions, points, is_hidden, test_mode)
        return test

    def __str__(self):
        return self.name


class TestSolution(models.Model):

    SOLUTION_STATUS = [('await', 'AWAIT VERIFICATION'), ('verified', 'VERIFIED')]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_solutions', null=False)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='test_solutions', null=False)
    answers: list[str] = SchemaField(default=[])
    score = models.IntegerField()
    status = models.CharField(max_length=30, choices=SOLUTION_STATUS, default='AWAIT VERIFICATION')


admin.site.register(Test)
