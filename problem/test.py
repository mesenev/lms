from django.urls import reverse
from model_mommy import mommy
from rest_framework import status

from imcslms.test import MainSetup
from course.models import Course
from lesson.models import Lesson
from problem.models import Problem, Submit
from problem.serializers import ProblemSerializer, ProblemListSerializer
from users.models import CourseAssignTeacher, CourseAssignStudent


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
        self.assertEqual(Problem.objects.count(), amount + 1)

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

    def test_problem_stats(self):
        teacher = self.test_setup()
        student = self.test_setup(group='student', username='test_user')
        (course := mommy.make(Course)).save()
        course.author = teacher
        CourseAssignTeacher(course=course, user=teacher).save()
        CourseAssignStudent(course=course, user=student).save()
        (lesson := mommy.make(Lesson, course=course, scores={'CW': 50, 'HW': 50, 'EX': 10})).save()
        (problem := mommy.make(Problem, type='CW')).save()
        problem.lesson = lesson
        problem.save()
        for new_status in ['AW', 'OK', 'WA', 'AW']:
            (submit_by_student := mommy.make(Submit, problem=problem, student=student, status=new_status)).save()
            (submit_by_teacher := mommy.make(Submit, problem=problem, student=teacher, status='AW')).save()
        url = reverse('problem-detail', kwargs=dict(pk=problem.id))
        self.client.force_authenticate(user=teacher)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('submits')), 8)
        self.assertEqual(response.data.get('stats')['green'], 1)
        self.assertEqual(response.data.get('stats')['red'], 0)

        url = reverse('problem-detail', kwargs=dict(pk=-1))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_course(self):
        pass
