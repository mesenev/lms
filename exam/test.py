from django.test import TestCase
from imcslms.test import MainSetup
from model_bakery import baker
from exam.models import ExaminationForm


class TestExams(MainSetup):
    
    def test_create_test(self):
        print(baker.make(ExaminationForm))
        