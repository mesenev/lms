from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from imcslms.test import MainSetup
from course.models import Course
from lesson.models import Lesson
from problem.models import Problem, Submit
from problem.serializers import ProblemSerializer, ProblemListSerializer

from group.models import CourseGroup
from users.models import CourseGroupAssignStudent, CourseGroupAssignTeacher


class ProblemTests(MainSetup):
    def test_create_problem(self):
        self.test_setup()
        (course := baker.make(Course, author=self.user)).save()
        baker.make(Lesson, course=course).save()
        instance = baker.make(Problem)
        instance.lesson = Lesson.objects.first()
        instance.save()
        data = ProblemSerializer(instance).data
        url = reverse('problem-list')
        amount = Problem.objects.count()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Problem.objects.count(), amount + 1)

    def test_delete_problem(self):
        self.test_setup()
        (course := baker.make(Course, author=self.user)).save()
        baker.make(Lesson, course=course).save()
        instance = baker.make(Problem)
        instance.lesson = Lesson.objects.first()
        instance.save()
        data = ProblemSerializer(instance).data
        url = reverse('problem-detail', kwargs=dict(pk=instance.id))
        amount = Problem.objects.count()
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Problem.objects.count(), amount - 1)

    def test_update_problem(self):
        self.test_setup()
        (course := baker.make(Course, author=self.user)).save()
        baker.make(Lesson, course=course).save()
        instance = baker.make(Problem)
        instance.lesson = Lesson.objects.first()
        instance.save()
        data = ProblemSerializer(instance).data
        data['id'] = instance.id
        data['lesson'] = instance.lesson.id
        url = reverse('problem-detail', kwargs=dict(pk=instance.id))
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_problem_stats(self):
        teacher = self.test_setup()
        student = self.test_setup(group='student', username='test_user')
        course = baker.make(Course)
        course.author = teacher

        course_group = baker.make(CourseGroup, course = course)

        course_group.staff.add(teacher)
        course_group.students.add(student)
        (lesson := baker.make(Lesson, course=course, scores={'CW': 50, 'HW': 50, 'EX': 10})).save()
        (problem := baker.make(Problem, type='CW')).save()
        problem.lesson = lesson
        problem.save()
        for new_status in ['AW', 'OK', 'WA', 'AW']:
            (submit_by_student := baker.make(Submit, problem=problem, student=student, status=new_status)).save()
            (submit_by_teacher := baker.make(Submit, problem=problem, student=teacher, status='AW')).save()
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
