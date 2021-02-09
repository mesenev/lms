import json

from django.urls import reverse

from rest_framework import status
from course.models import Course
from course.serializers import CourseSerializer
from imcslms.test import MainSetup
from model_mommy import mommy


class CourseTests(MainSetup):
    def test_create_course(self):
        self.test_setup()
        data = CourseSerializer(mommy.make(Course)).data
        url = reverse('course-list')
        # data = json.dumps(data)
        amount = Course.objects.count()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), amount + 1)
