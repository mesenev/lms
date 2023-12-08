from django.test import TestCase
from imcslms.test import MainSetup
from group.models import Group
from course.models import Course
from group.serializers import GroupSerializer
from model_bakery import baker
from django.urls import reverse
from rest_framework import status


class ProblemTests(MainSetup):
     def test_create_problem(self):
         self.test_setup()
         (course := baker.make(Course)).save()
         instance = baker.make(Group)
         instance.course = Course.objects.first()
         instance.save()
         data = GroupSerializer(instance).data
         url = reverse('group-list')
         amount = Group.objects.count()
         response = self.client.post(url, data, format='json')
         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
         self.assertEqual(Group.objects.count(), amount + 1)
