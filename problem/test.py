from django.urls import reverse
from model_mommy import mommy
from rest_framework import status

from imcslms.test import MainSetup
from course.models import Course
from lesson.models import Lesson
from problem.models import Problem
from problem.serializers import ProblemSerializer
from users.models import CourseAssignTeacher


class ProblemTests(MainSetup):
    def test_create_problem(self):
        self.test_setup()
        (course := mommy.make(Course)).save()
        mommy.make(Lesson, course=course).save()
        instance = mommy.make(Problem)
        instance.lesson = Lesson.objects.first()
        instance.save()
        data = ProblemSerializer(instance).data
        url = reverse('problem-list')
        amount = Problem.objects.count()
        CourseAssignTeacher(course=course, user=self.user).save()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Problem.objects.count(), amount+1)

    def test_delete_problem(self):
        self.test_setup()
        (course := mommy.make(Course)).save()
        mommy.make(Lesson, course=course).save()
        instance = mommy.make(Problem)
        instance.lesson = Lesson.objects.first()
        instance.save()
        data = ProblemSerializer(instance).data
        url = reverse('problem-detail', kwargs=dict(pk=instance.id))
        amount = Problem.objects.count()
        CourseAssignTeacher(course=course, user=self.user).save()
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Problem.objects.count(), amount - 1)

    def test_update_problem(self):
        self.test_setup()
        (course := mommy.make(Course)).save()
        mommy.make(Lesson, course=course).save()
        instance = mommy.make(Problem)
        instance.lesson = Lesson.objects.first()
        instance.save()
        data = ProblemSerializer(instance).data
        data['id'] = instance.id
        data['lesson'] = instance.lesson.id
        url = reverse('problem-detail', kwargs=dict(pk=instance.id))
        CourseAssignTeacher(course=course, user=self.user).save()
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_course(self):
        pass

