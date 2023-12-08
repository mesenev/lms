from django.test import TestCase
from imcslms.test import MainSetup
from group.models import Group
from course.models import Course
from group.serializers import GroupSerializer
from model_bakery import baker
from django.urls import reverse
from rest_framework import status
from users.models import GroupAssignTeacher
from users.serializers import DefaultUserSerializer


class ProblemTests(MainSetup):
     def test_create_group(self):
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

     def test_assign_teacher(self):

         self.test_setup()
         (group := baker.make(Group)).save()

         url = reverse('group-detail', kwargs=dict(pk=group.id)) + "assign-teacher/"
         data = DefaultUserSerializer(self.user).data
         response = self.client.post(url, data, format='json')

         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.assertEqual(Group.objects.first(), self.user.staff_for.first())
         self.assertEqual(self.user, Group.objects.first().staff.first())

     def test_assign_student(self):
         self.test_setup(group='student')
         (group := baker.make(Group)).save()

         url = reverse('group-detail', kwargs=dict(pk=group.id)) + "assign-student/"
         data = DefaultUserSerializer(self.user).data
         response = self.client.post(url, data, format='json')

         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.assertEqual(Group.objects.first(), self.user.student_for.first())
         self.assertEqual(self.user, Group.objects.first().students.first())


