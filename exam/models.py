from django.db import models
from django.contrib import admin
from lesson.models import Lesson
import pydantic
from django_pydantic_field import SchemaField
from users.models import User
from pydantic import validate_arguments


class UserAnswerToQuestion(pydantic.BaseModel):
    question_index: int
    submitted_answers: list[str] = []


class Question(pydantic.BaseModel):
    index: int = 0
    text: str
    description: str = ''
    correct_answers: list[str] = []
    all_answers: list[str] = []
    answer_type: str
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
    description = models.TextField(default='')
    questions = models.JSONField()
    points = models.IntegerField()
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
    score = models.IntegerField()
    status = models.CharField(max_length=30, choices=SOLUTION_STATUS, default='AWAIT VERIFICATION')
    correct_questions_indexes = models.JSONField(default=[])

    @classmethod
    @validate_arguments
    def create(cls, student, exam, user_answers: list[UserAnswerToQuestion], score, status,
               correct_questions_indexes:list[int]
               ):
        solution = cls(student, exam, user_answers, score, status, correct_questions_indexes)
        return solution


admin.site.register(ExaminationForm)
admin.site.register(ExamSolution)
