from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from group import main as setup_groups


class MainSetup(APITestCase):
    def test_setup(self):
        setup_groups()
        my_group = Group.objects.get(name='teacher')
        self.user = get_user_model().objects.create_user(
            'ksarthak4eve',
            'hakunamatata',
            'password1234'
        )
        my_group.user_set.add(self.user)
        self.client.login(username=self.user.username, password='password1234')
        # self.client.force_authenticate(self.user)
