from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from course.models import Course, CourseSchedule
from lesson.serializers import LessonSerializer, AttachmentSerializer
from imcslms.test import MainSetup
from lesson.models import Lesson, LessonContent, Attachment
from users.models import CourseAssignTeacher


class LessonTests(MainSetup):
    def test_create_lesson(self):
        self.test_setup()
        data = LessonSerializer(baker.make(Lesson)).data
        url = reverse('lesson-list')
        amount = Lesson.objects.count()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), amount + 1)

    def test_delete_lesson(self):
        self.test_setup()
        (course := baker.make(Course)).save()
        baker.make(Lesson, course=course).save()
        lesson = Lesson.objects.first()
        CourseAssignTeacher(course=course, user=self.user).save()
        CourseSchedule(course=course).save()
        data = LessonSerializer(baker.make(Lesson)).data
        url = reverse('lesson-detail', kwargs=dict(pk=lesson.id))
        data['id'] = lesson.id
        amount = Lesson.objects.count()
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), amount - 1)

    def test_update_lesson(self):
        self.test_setup()
        (course := baker.make(Course)).save()
        baker.make(Lesson, course=course).save()
        lesson = Lesson.objects.first()
        CourseAssignTeacher(course=course, user=self.user).save()
        data = LessonSerializer(baker.make(Lesson)).data
        url = reverse(
            'lesson-detail',
            kwargs=dict(pk=lesson.id)
        )
        data['id'] = lesson.id
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson_no_assignment(self):
        self.test_setup()
        (course := baker.make(Course)).save()
        baker.make(Lesson, course=course).save()
        lesson = Lesson.objects.first()
        data = LessonSerializer(baker.make(Lesson)).data
        url = reverse(
            'lesson-detail',
            kwargs=dict(pk=lesson.id)
        )
        data['id'] = lesson.id
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_lesson(self):
        pass


class AttachmentsTests(MainSetup):

    def test_create_attachment(self):

        self.test_setup()

        baker_model = baker.make(Attachment, _fill_optional=True)

        attachment = AttachmentSerializer(baker_model).data
        test_file = SimpleUploadedFile('test_file', b'ttttt')
        attachment['file_url'] = test_file
        amount = Attachment.objects.count()

        response = self.client.post('/api/attachments/', data=attachment)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attachment.objects.count(), amount + 1)
        Attachment.objects.all().delete()

    def test_delete_attachment(self):

        self.test_setup()
