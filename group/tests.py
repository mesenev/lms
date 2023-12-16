from django.test import TestCase
from imcslms.test import MainSetup
from group.models import CourseGroup, CourseGroupLink
from course.models import Course
from group.serializers import CourseGroupSerializer, CourseGroupLinkSerializer
from model_bakery import baker
from django.urls import reverse
from rest_framework import status
from users.models import CourseGroupAssignTeacher, User, CourseGroupAssignStudent
from users.serializers import DefaultUserSerializer
from django.contrib.auth.models import Group as PermissionsGroup


class GroupTests(MainSetup):
     def test_create_group(self):
         self.test_setup()
         baker.make(Course).save()
         instance = baker.make(PermissionsGroup)
         instance.course = Course.objects.first()
         instance.save()
         data = CourseGroupSerializer(instance).data
         url = reverse('group-list')
         amount = CourseGroup.objects.count()
         response = self.client.post(url, data, format='json')
         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
         self.assertEqual(CourseGroup.objects.count(), amount + 1)

     def test_assign_teacher(self):
         self.test_setup()

         baker.make(Course).save()
         group = baker.make(CourseGroup)
         group.course = Course.objects.first()
         group.save()

         CourseGroupAssignTeacher.objects.create(user=self.user, group=group).save()

         new_teacher_user=baker.make(User)
         PermissionsGroup.objects.get(name='teacher').user_set.add(new_teacher_user)

         url = reverse('group-detail', kwargs=dict(pk=group.id)) + "assign-teacher/"
         data = DefaultUserSerializer(new_teacher_user).data
         response = self.client.post(url, data, format='json')

         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.assertEqual(CourseGroup.objects.first(), self.user.staff_for.first())
         self.assertEqual(self.user, CourseGroup.objects.first().staff.first())

     def test_assign_student(self):
         self.test_setup()

         baker.make(Course).save()
         group = baker.make(CourseGroup)
         group.course = Course.objects.first()
         group.save()

         CourseGroupAssignTeacher.objects.create(user=self.user, group=group).save()

         new_student_user = baker.make(User)
         PermissionsGroup.objects.get(name='student').user_set.add(new_student_user)

         url = reverse('group-detail', kwargs=dict(pk=group.id)) + "assign-student/"
         data = DefaultUserSerializer(new_student_user).data
         response = self.client.post(url, data, format='json')

         new_student_user = User.objects.get(id=new_student_user.id)

         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.assertEqual(CourseGroup.objects.first(), new_student_user.student_for.first())
         self.assertEqual(new_student_user, CourseGroup.objects.first().students.first())

     def test_delete_teacher_from_group(self):
         self.test_setup()

         baker.make(Course).save()
         group = baker.make(PermissionsGroup)
         group.course = Course.objects.first()
         group.save()

         CourseGroupAssignTeacher.objects.create(user=self.user, group=group).save()

         new_teacher_user = baker.make(User)
         PermissionsGroup.objects.get(name='teacher').user_set.add(new_teacher_user)
         CourseGroupAssignTeacher.objects.create(user=new_teacher_user, group=group).save()
         count = CourseGroupAssignTeacher.objects.count()

         url = reverse('group-detail', kwargs=dict(pk=group.id)) + "delete-teacher/"
         data = DefaultUserSerializer(new_teacher_user).data
         response = self.client.delete(url, data, format='json')

         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.assertEqual(count-1, CourseGroupAssignTeacher.objects.count())
         self.assertEqual(CourseGroup.objects.get(id=group.id).staff.count(), 1)
         self.assertEqual(User.objects.get(id=new_teacher_user.id).staff_for.count(), 0)

     def test_delete_student_from_group(self):
         self.test_setup()
         baker.make(Course).save()
         group = baker.make(CourseGroup)
         group.course = Course.objects.first()
         group.save()

         CourseGroupAssignTeacher.objects.create(user=self.user, group=group).save()

         new_student_user = baker.make(User)
         PermissionsGroup.objects.get(name='student').user_set.add(new_student_user)

         CourseGroupAssignStudent.objects.create(user=new_student_user, group=group).save()

         data = DefaultUserSerializer(new_student_user).data
         url = reverse('group-detail', kwargs=dict(pk=group.id)) + "delete-student/"
         response = self.client.delete(url, data, format='json')

         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.assertEqual(User.objects.get(id=new_student_user.id).student_for.count(), 0)
         self.assertEqual(CourseGroup.objects.get(id=group.id).students.count(), 0)






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

