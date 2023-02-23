from django.test import TestCase
from imcslms.test import MainSetup
from model_bakery import baker
from test.models import Test


class TestTests(MainSetup):
    
    def test_create_test(self):
        print(baker.make(Test))
        