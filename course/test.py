from django.urls import reverse
from model_mommy import mommy
from rest_framework import status

from course.models import Course
from course.serializers import CourseSerializer
from imcslms.test import MainSetup


class CourseTests(MainSetup):
    def test_create_course(self):
        self.test_setup()
        data = CourseSerializer(mommy.make(Course)).data
        url = reverse('course-list')
        amount = Course.objects.count()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), amount + 1)

    def test_update_course(self):
        self.test_setup()
        mommy.make(Course).save()
        instance = Course.objects.first()
        data = CourseSerializer(instance).data
        data['id'] = instance.id
        url = reverse('course-detail', kwargs=dict(pk=instance.id))
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_course(self):
        self.test_setup()
        instance = mommy.make(Course)
        data = CourseSerializer(instance).data
        url = reverse('course-detail', kwargs=dict(pk=instance.id))
        amount = Course.objects.count()
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), amount - 1)

    def test_read_course(self):
        self.test_setup()
        url = reverse('course-list')
        amount = Course.objects.count()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
