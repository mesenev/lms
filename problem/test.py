from django.urls import reverse

from rest_framework import status
from problem.models import Problem
from problem.serializers import ProblemSerializer
from imcslms.test import MainSetup
from model_mommy import mommy


class ProblemTests(MainSetup):
    def test_create_problem(self):
        self.test_setup()
        data = ProblemSerializer(mommy.make(Problem)).data
        url = reverse('problem-list')
        amount = Problem.objects.count()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Problem.objects.count(), amount + 1)

    def test_delete_problem(self):
        self.test_setup()
        data = ProblemSerializer(mommy.make(Problem)).data
        url = reverse('problem-list')
        amount = Problem.objects.count()
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Problem.objects.count(), amount - 1)

    def test_update_problem(self):
        self.test_setup()
        data = ProblemSerializer(mommy.make(Problem)).data
        url = reverse('course-list')
        amount = Problem.objects.count()
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_read_course(self):
        pass

