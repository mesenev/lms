from django.urls import reverse

from rest_framework import status
from users.models import User
from users.serializers import DefaultUserSerializer
from imcslms.test import MainSetup
from model_mommy import mommy


class UserTests(MainSetup):
    def test_user_login(self):
        pass

    def test_user_logout(self):
        pass

    def test_user_change_password(self):
        pass
