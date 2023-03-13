from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from course.models import Course
from imcslms.test import MainSetup
from lesson.models import Lesson
from problem.models import Problem, Submit
from rating.models import CourseProgress, LessonProgress
from rating.serializers import CourseProgressSerializer, LessonProgressSerializer
from users.models import CourseAssignTeacher, CourseAssignStudent


class CourseProgressTests(MainSetup):
    def test_course_progress_access(self):
        teacher = self.test_setup()
        students = [self.test_setup(group='student', username=f'test_user{i}') for i in range(10)]
        (course := baker.make(Course, author=teacher)).save()
        CourseAssignTeacher(course=course, user=teacher).save()
        for student in students:
            CourseAssignStudent(course=course, user=student).save()
        (lesson := baker.make(Lesson, course=course, scores={'CW': 50, 'HW': 50, 'EX': 10})).save()
        (problem := baker.make(Problem, type='CW', lesson=lesson)).save()

        submits_by_students = []
        for i in range(len(students)):
            submits_by_students.append(baker.make(Submit, problem=problem, student=students[i], status='OK'))
            submits_by_students[i].save()

        (submit_by_teacher := baker.make(Submit, problem=problem, student=teacher, status='OK')).save()
        self.client.force_authenticate(user=teacher)
        url = reverse('courseprogress-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(students))
        progress = response.data[0].get('progress')
        self.assertEqual(progress[list(progress.keys())[0]]['CW'], 50.0)

        url = reverse('courseprogress-detail', kwargs=dict(pk=-1))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        instance = CourseProgress.objects.filter(course_id=course.id).first()

        url = reverse('courseprogress-detail', kwargs=dict(pk=instance.id))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course_progress(self):
        teacher = self.test_setup()
        students = [self.test_setup(group='student', username=f'test_user{i}') for i in range(2)]
        (course := baker.make(Course)).save()
        (lesson := baker.make(Lesson, course=course)).save()
        (instance := baker.make(CourseProgress, course=course, user=students[0])).save()
        data = CourseProgressSerializer(instance).data
        CourseAssignTeacher(course=course, user=teacher).save()
        data['user'] = students[1].id
        url = reverse('courseprogress-list')
        amount = CourseProgress.objects.count()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CourseProgress.objects.count(), amount + 1)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CourseProgress.objects.count(), amount + 1)

        data['user'] = -1
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CourseProgress.objects.count(), amount + 1)

    def test_update_course_progress(self):
        def check(check_status, data):
            response = self.client.patch(url, data, format='json')
            self.assertEqual(response.status_code, check_status)

        teacher = self.test_setup()
        students = [self.test_setup(group='student', username=f'test_user{i}') for i in range(2)]
        self.user = teacher
        self.client.user = self.user
        self.client.force_authenticate(user=self.user)

        (course := baker.make(Course)).save()
        CourseAssignTeacher(course=course, user=teacher).save()
        (lesson := baker.make(Lesson, course=course)).save()
        (instance := baker.make(CourseProgress, user=students[0], course=course)).save()
        data = CourseProgressSerializer(instance).data
        data['id'] = instance.id
        data['user'] = instance.user.id

        url = reverse('courseprogress-detail', kwargs={'pk': instance.id})
        check(status.HTTP_200_OK, data)

        url = reverse('courseprogress-detail', kwargs={'pk': -1})
        check(status.HTTP_404_NOT_FOUND, data)

        data = CourseProgressSerializer(instance).data
        url = reverse('courseprogress-detail', kwargs={'pk': instance.id})
        check(status.HTTP_200_OK, data)

    def test_delete_course_progress(self):
        teacher = self.test_setup()
        students = [self.test_setup(group='student', username=f'test_user{i}') for i in range(2)]

        self.user = teacher
        self.client.user = self.user
        self.client.force_authenticate(user=self.user)

        (course := baker.make(Course)).save()
        CourseAssignTeacher(course=course, user=teacher).save()
        (lesson := baker.make(Lesson, course=course)).save()
        (instance := baker.make(CourseProgress, user=students[0], course=course)).save()
        data = CourseProgressSerializer(instance).data
        data['id'] = instance.id
        data['user'] = instance.user.id
        amount = CourseProgress.objects.count()
        url = reverse('courseprogress-detail', kwargs={'pk': instance.id})
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Problem.objects.count(), amount - 1)
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class LessonProgressTests(MainSetup):
    def test_lesson_progress_access(self):
        def check_access(filter_type, id, submit: Submit = None):
            url = f'/api/lessonprogress/?{filter_type}_id={id}'
            response = self.client.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            if submit is not None:
                submit_status_by_resp = response.data[0].get('solved').get('CW').get(str(submit.problem.id))
                self.assertEqual(submit_status_by_resp, [submit.status, submit.id])

            url = f'/api/lessonprogress/?{filter_type}_id=-1'
            response = self.client.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        teacher = self.test_setup()
        students = [self.test_setup(group='student', username=f'test_user{i}') for i in range(10)]

        self.user = teacher
        self.client.user = self.user
        self.client.force_authenticate(user=self.user)
        (course := baker.make(Course, author=teacher)).save()
        CourseAssignTeacher(course=course, user=teacher).save()
        for student in students:
            CourseAssignStudent(course=course, user=student).save()
        (lesson := baker.make(Lesson, course=course, scores={'CW': 50, 'HW': 50, 'EX': 10})).save()
        (problem := baker.make(Problem, type='CW', lesson=lesson)).save()
        submits_by_students = []
        for i in range(len(students)):
            submits_by_students.append(baker.make(Submit, problem=problem, student=students[i], status='OK'))
            submits_by_students[i].save()
        for i in range(len(students)):
            submits_by_students.append(baker.make(Submit, problem=problem, student=students[i], status='WA'))
            submits_by_students[i].save()
        (submit_by_teacher := baker.make(Submit, problem=problem, student=teacher, status='OK')).save()
        self.client.force_authenticate(user=teacher)

        check_access('lesson', lesson.id)
        check_access('lesson', lesson.id, submit=submits_by_students[0])
        check_access('course', course.id)
        check_access('problem', problem.id)

        url = reverse('lessonprogress-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_lesson_progress(self):
        def check(check_status):
            self.assertEqual(response.status_code, check_status)
            self.assertEqual(LessonProgress.objects.count(), amount + 1)

        teacher = self.test_setup()
        students = [self.test_setup(group='student', username=f'test_user{i}') for i in range(2)]
        self.user = teacher
        self.client.user = self.user
        self.client.force_authenticate(user=self.user)

        (course := baker.make(Course)).save()
        (lesson := baker.make(Lesson, course=course)).save()
        (instance := baker.make(LessonProgress, attendance=True, user=students[0], lesson=lesson)).save()
        data = LessonProgressSerializer(instance).data
        data['user'] = students[1].id
        url = reverse('lessonprogress-list')
        amount = LessonProgress.objects.count()
        CourseAssignTeacher(course=course, user=teacher).save()
        response = self.client.post(url, data, format='json')
        check(status.HTTP_201_CREATED)

        response = self.client.post(url, data, format='json')
        check(status.HTTP_400_BAD_REQUEST)

        data['user'] = -1
        response = self.client.post(url, data, format='json')
        check(status.HTTP_400_BAD_REQUEST)

        data['attendance'] = -1
        response = self.client.post(url, data, format='json')
        check(status.HTTP_400_BAD_REQUEST)

        data['solved'] = -1
        response = self.client.post(url, data, format='json')
        check(status.HTTP_400_BAD_REQUEST)

    def test_update_lesson_progress(self):
        def check(check_status, data):
            response = self.client.patch(url, data, format='json')
            self.assertEqual(response.status_code, check_status)

        teacher = self.test_setup()
        students = [self.test_setup(group='student', username=f'test_user{i}') for i in range(2)]
        self.user = teacher
        self.client.user = self.user
        self.client.force_authenticate(user=self.user)

        (course := baker.make(Course)).save()
        CourseAssignTeacher(course=course, user=teacher).save()
        (lesson := baker.make(Lesson, course=course)).save()
        (instance := baker.make(LessonProgress, user=students[0], lesson=lesson)).save()
        data = LessonProgressSerializer(instance).data
        data['id'] = instance.id
        data['lesson'] = instance.lesson.id

        url = reverse('lessonprogress-detail', kwargs={'pk': instance.id})
        check(status.HTTP_200_OK, data)

        url = reverse('lessonprogress-detail', kwargs={'pk': -1})
        check(status.HTTP_404_NOT_FOUND, data)

        data = LessonProgressSerializer(instance).data
        url = reverse('lessonprogress-detail', kwargs={'pk': instance.id})
        check(status.HTTP_200_OK, data)

    def test_delete_lesson_progress(self):
        teacher = self.test_setup()
        students = [self.test_setup(group='student', username=f'test_user{i}') for i in range(2)]
        self.user = teacher
        self.client.user = self.user
        self.client.force_authenticate(user=self.user)

        (course := baker.make(Course)).save()
        (lesson := baker.make(Lesson, course=course)).save()
        (instance := baker.make(LessonProgress, attendance=True, user=students[0], lesson=lesson)).save()
        data = LessonProgressSerializer(instance).data
        data['user'] = students[1].id
        amount = LessonProgress.objects.count()
        CourseAssignTeacher(course=course, user=teacher).save()
        CourseAssignStudent(course=course, user=students[1]).save()
        url = reverse('lessonprogress-detail', kwargs={'pk': instance.id})
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Problem.objects.count(), amount - 1)
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
