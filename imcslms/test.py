from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase


class MainSetup(APITestCase):
    def test_setup(self):
        my_group = Group.objects.get(name='teacher')
        self.user = get_user_model().objects.create_user(
            'ksarthak4eve',
            'hakunamatata',
            'password1234'
        )
        my_group.user_set.add(self.user)
        self.client.login(username=self.user.username, password='password1234')
        self.client.force_authenticate(user=self.user)
        return
