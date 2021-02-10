

from django.urls import reverse

from rest_framework import status
from lesson.models import Lesson
from course.serializers import LessonSerializer
from imcslms.test import MainSetup
from model_mommy import mommy


class LessonTests(MainSetup):
    def test_create_lesson(self):
        self.test_setup()
        data = LessonSerializer(mommy.make(Lesson)).data
        url = reverse('lesson-list')
        amount = Lesson.objects.count()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), amount + 1)

    def test_delete_lesson(self):
        self.test_setup()
        data = LessonSerializer(mommy.make(Lesson)).data
        url = reverse('lesson-list')
        # data = json.dumps(data)
        amount = Lesson.objects.count()
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), amount - 1)

    def test_update_lesson(self):
        self.test_setup()
        data = LessonSerializer(mommy.make(Lesson)).data
        url = reverse('lesson-list')
        # data = json.dumps(data)
        amount = Lesson.objects.count()
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_lesson(self):
        pass
