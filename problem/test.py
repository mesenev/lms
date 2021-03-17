from django.urls import reverse
from model_mommy import mommy
from rest_framework import status

from imcslms.test import MainSetup
from lesson.models import Lesson
from problem.models import Problem
from problem.serializers import ProblemSerializer


class ProblemTests(MainSetup):
    def test_create_problem_without_lesson(self):
        self.test_setup()
        data = ProblemSerializer(mommy.make(Problem)).data
        url = reverse('problem-list')
        amount = Problem.objects.count()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Problem.objects.count(), amount)

    def test_create_problem(self):
        self.test_setup()
        instance: Problem = mommy.make(Problem)
        lesson = mommy.make(Lesson)
        lesson.save()
        instance.lesson = Lesson.objects.all().first()
        data = ProblemSerializer(instance).data
        url = reverse('problem-list')
        amount = Problem.objects.count()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Problem.objects.count(), amount + 1)

    def test_delete_problem(self):
        self.test_setup()
        self.client.force_authenticate(user=self.user)
        mommy.make(Problem).save()
        problem = Problem.objects.all().first()
        url = reverse('problem-detail', kwargs=dict(pk=problem.id))
        amount = Problem.objects.count()
        response = self.client.delete(url, {'id': problem.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Problem.objects.count(), amount - 1)

    def test_update_problem(self):
        self.test_setup()
        mommy.make(Lesson).save()
        problem = mommy.make(Problem)
        problem.lesson = Lesson.objects.first()
        problem.save()
        data = ProblemSerializer(mommy.make(Problem)).data
        data['id'] = problem.id
        data['lesson'] = problem.lesson.id
        url = reverse('problem-detail', kwargs=dict(pk=problem.id))
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_course(self):
        pass

