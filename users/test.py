from django.urls import reverse

from rest_framework import status
from users.models import User
from users.serializers import DefaultUserSerializer
from imcslms.test import MainSetup
from model_bakery import baker


class UserTests(MainSetup):

    def test_user_change_password(self):
        pass

    def test_user_change_avatar(self):
        pass
