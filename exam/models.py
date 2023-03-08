from django.db import models
from django.contrib import admin
from lesson.models import Lesson
import pydantic
from django_pydantic_field import SchemaField
from users.models import User
from pydantic import validate_arguments
from enum import Enum


class AnswerTypes(str, Enum):
    input = 'input'
    text = 'text'
    radio = 'radio'
    checkbox = 'checkbox'

class AnswerVerdictTypes(str, Enum):
    correct = 'correct'
    incorrect = 'incorrect'
    await_verification = 'await_verification'

class UserAnswerToQuestion(pydantic.BaseModel):
    question_index: int
    submitted_answers: list[str] = []


class Question(pydantic.BaseModel):
    index: int = 0
    text: str
    description: str = ''
    correct_answers: list[str] = []
    all_answers: list[str] = []
    answer_type: AnswerTypes
    attachment_url: str = ''
    points: int


class ExaminationForm(models.Model):
    TEST_MODE_TYPES = [
        ('auto', 'Automated only testing'),
        ('manual', 'Manual only testing'),
        ('auto_and_manual', 'Manual then automated testing')
    ]

    name = models.CharField(max_length=500)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, related_name='exams', null=True)
    description = models.TextField(blank=True)
    questions = models.JSONField()
    max_points = models.IntegerField()
    is_hidden = models.BooleanField(default=True)
    test_mode = models.CharField(max_length=30, choices=TEST_MODE_TYPES, default=TEST_MODE_TYPES[0][0])

    @classmethod
    @validate_arguments
    def create(cls, name, lesson, description, questions: list[Question], points, is_hidden, test_mode):
        exam = cls(name, lesson, description, questions, points, is_hidden, test_mode)
        return exam

    def __str__(self):
        return self.name


class ExamSolution(models.Model):

    SOLUTION_STATUS = [('await', 'AWAIT VERIFICATION'), ('verified', 'VERIFIED')]
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_solutions', null=False)
    exam = models.ForeignKey(ExaminationForm, on_delete=models.CASCADE, related_name='exam_solutions', null=False)
    user_answers = models.JSONField(default=[])
    solution_points = models.IntegerField()
    status = models.CharField(max_length=30, choices=SOLUTION_STATUS, default='await')
    question_verdicts = models.JSONField(default=[])

    @classmethod
    @validate_arguments
    def create(cls, student, exam, user_answers: list[UserAnswerToQuestion], score, status,
               question_verdicts: dict[int, AnswerVerdictTypes]
               ):
        solution = cls(student, exam, user_answers, score, status, question_verdicts)
        return solution


admin.site.register(ExaminationForm)
admin.site.register(ExamSolution)
