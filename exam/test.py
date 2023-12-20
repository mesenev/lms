# from django.test import TestCase
# from django.urls import reverse
# from rest_framework import status
# from imcslms.test import MainSetup
# from model_bakery import baker
# from course.models import Course
# from lesson.models import Lesson
# from exam.models import ExaminationForm, ExamSolution
# from exam.serializers import ExamSerializer, ExamSolutionSerializer
# from users.models import CourseAssignTeacher, CourseAssignStudent
#
#
# class TestExams(MainSetup):
#
#     def test_create_exam(self):
#         self.test_setup()
#         baker.make(Course).save()
#         crs = Course.objects.first()
#         baker.make(Lesson, course=crs).save()
#         lsn = Lesson.objects.first()
#
#         data = ExamSerializer(baker.make(ExaminationForm, lesson=lsn)).data
#         amount = ExaminationForm.objects.count()
#
#         response = self.client.post(reverse('exam-list'), data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(amount + 1, ExaminationForm.objects.count())
#
#     def test_student_cant_create_exam(self):
#         self.test_setup(group='student')
#         baker.make(Course).save()
#         crs = Course.objects.first()
#         baker.make(Lesson, course=crs).save()
#         lsn = Lesson.objects.first()
#
#         data = ExamSerializer(baker.make(ExaminationForm, lesson=lsn)).data
#         amount = ExaminationForm.objects.count()
#
#         response = self.client.post(reverse('exam-list'), data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(amount, ExaminationForm.objects.count())
#
#
# class TestExamSolution(MainSetup):
#
#     def test_create_solution(self):
#         self.test_setup(group='student')
#         baker.make(Course).save()
#         crs = Course.objects.first()
#         baker.make(Lesson, course=crs).save()
#         lsn = Lesson.objects.first()
#         exam = baker.make(ExaminationForm, lesson=lsn)
#         data = ExamSolutionSerializer(baker.make(ExamSolution, exam=exam)).data
#
#         amount = ExamSolution.objects.count()
#         response = self.client.post(reverse('exam_solution-list'), data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(amount + 1, ExamSolution.objects.count())
#
#     def test_update_solution(self):
#         self.test_setup()
#         baker.make(Course).save()
#         crs = Course.objects.first()
#         baker.make(Lesson, course=crs).save()
#         lsn = Lesson.objects.first()
#         exam = baker.make(ExaminationForm, lesson=lsn)
#         CourseAssignTeacher(course=crs, user=self.user).save()
#
#         solution = baker.make(ExamSolution, exam=exam, student=self.user)
#         data = ExamSolutionSerializer(solution).data
#
#         response = self.client.patch(reverse('exam_solution-detail', kwargs=dict(pk=solution.id)), data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_student_cant_update_solution(self):
#         self.test_setup(group='student')
#         baker.make(Course).save()
#         crs = Course.objects.first()
#         baker.make(Lesson, course=crs).save()
#         lsn = Lesson.objects.first()
#         exam = baker.make(ExaminationForm, lesson=lsn)
#         CourseAssignStudent(course=crs, user=self.user).save()
#
#         solution = baker.make(ExamSolution, exam=exam, student=self.user)
#         data = ExamSolutionSerializer(solution).data
#
#         response = self.client.patch(reverse('exam_solution-detail', kwargs=dict(pk=solution.id)), data)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_student_cant_attempt_limit_exceeded(self):
#         self.test_setup(group='student')
#         baker.make(Course).save()
#         crs = Course.objects.first()
#         baker.make(Lesson, course=crs).save()
#         lsn = Lesson.objects.first()
#         exam = baker.make(ExaminationForm, lesson=lsn)
#         data = ExamSolutionSerializer(baker.make(ExamSolution, exam=exam)).data
#
#         response = self.client.post(reverse('exam_solution-list'), data, format='json')
#         amount = ExamSolution.objects.count()
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#         response = self.client.post(reverse('exam_solution-list'), data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
#         self.assertEqual(amount, ExamSolution.objects.count())