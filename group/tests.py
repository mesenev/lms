from django.test import TestCase
from imcslms.test import MainSetup
from group.models import Group, GroupLink
from course.models import Course
from group.serializers import GroupSerializer, LinkSerializer
from model_bakery import baker
from django.urls import reverse
from rest_framework import status
from users.models import GroupAssignTeacher, User
from users.serializers import DefaultUserSerializer
from django.contrib.auth.models import Group as PermissionsGroup


class GroupTests(MainSetup):
     def test_create_group(self):
         self.test_setup()
         baker.make(Course).save()
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

         baker.make(Course).save()
         group = baker.make(Group)
         group.course = Course.objects.first()
         group.save()

         GroupAssignTeacher.objects.create(user=self.user, group=group).save()

         new_teacher_user=baker.make(User)
         PermissionsGroup.objects.get(name='teacher').user_set.add(new_teacher_user)

         url = reverse('group-detail', kwargs=dict(pk=group.id)) + "assign-teacher/"
         data = DefaultUserSerializer(new_teacher_user).data
         response = self.client.post(url, data, format='json')

         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.assertEqual(Group.objects.first(), self.user.staff_for.first())
         self.assertEqual(self.user, Group.objects.first().staff.first())

     def test_assign_student(self):
         self.test_setup()

         baker.make(Course).save()
         group = baker.make(Group)
         group.course = Course.objects.first()
         group.save()

         GroupAssignTeacher.objects.create(user=self.user, group=group).save()

         new_student_user = baker.make(User)
         PermissionsGroup.objects.get(name='student').user_set.add(new_student_user)

         url = reverse('group-detail', kwargs=dict(pk=group.id)) + "assign-student/"
         data = DefaultUserSerializer(new_student_user).data
         response = self.client.post(url, data, format='json')

         new_student_user = User.objects.get(id=new_student_user.id)

         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.assertEqual(Group.objects.first(), new_student_user.student_for.first())
         self.assertEqual(new_student_user, Group.objects.first().students.first())

     # def test_create_link(self):
     #     self.test_setup(group='teacher')
     #     (group:= baker.make(Group)).save()
     #     instanse = baker.make(GroupLink)
     #     instanse.group = group
     #
     #     data = LinkSerializer(instanse).data
     #     url = reverse('group-list')
     #     response = self.client.post(url, data, format='json')
     #     l = [link for link in GroupLink.objects.all()]
     #     for item in l:
     #         print(LinkSerializer(item).data)
     #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
     #     self.assertEqual(group.id, GroupLink.objects.first().group.id)

