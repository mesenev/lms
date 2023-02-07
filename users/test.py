from django.urls import reverse
from django.core.files.images import ImageFile
from rest_framework import status
from users.models import User, content_file_name
from users.serializers import DefaultUserSerializer
from imcslms.test import MainSetup
from model_bakery import baker
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image


class UserTests(MainSetup):

    def test_user_change_password(self):
        pass

    def test_user_change_avatar(self):
        self.test_setup()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
        data = {'avatar_url': uploaded}
        response = self.client.post('/api/change-avatar/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

