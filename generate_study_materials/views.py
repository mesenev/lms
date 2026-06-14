from django.shortcuts import render
from generate_study_materials.AiModel import AiModel
from generate_study_materials.OpenAiModel import OpenAiModel
from django.http import HttpResponse
import os
import re
from .CourseRequestDto import CourseRequestDto
import json
from course.models import Course
from lesson.models import Lesson, LessonContent
from lesson.storages import gen_hash_name
from django.core.files.base import ContentFile
from exam.models import ExaminationForm

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from celery_app.tasks import generate_notes_for_lesson, generate_exam_for_lesson


class CourseGenerationApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        aiModel = AiModel()

        response = aiModel.generateCourse(
            CourseRequestDto(1, request.data.get('courseName'), "practice", 2,
                             0))
        clean_json = re.sub(r'^```json\s*|\s*```$', '', response.text.strip())
        parsed_response = json.loads(clean_json)
        newCourse = Course(name=parsed_response["courseTitle"],
                           description=parsed_response["courseSummary"],
                           cats_id=-1,
                           author=request.user)
        newCourse.save()

        for chapter in parsed_response['chapters']:
            newLesson = Lesson(course=newCourse,
                               name=chapter["chapterTitle"],
                               description=chapter["chapterSummary"],
                               author=request.user)
            newLesson.save()

            generate_notes_for_lesson.delay(newLesson.id, request.user.id)
            generate_exam_for_lesson.delay(newLesson.id)



        return HttpResponse("OK", status=200)
