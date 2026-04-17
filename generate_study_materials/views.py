from django.shortcuts import render
from generate_study_materials.AiModel import AiModel
from django.http import HttpResponse
from google.genai import types
import os
from .CourseRequestDto import CourseRequestDto
import json
from course.models import Course
from lesson.models import Lesson, LessonContent
from lesson.storages import gen_hash_name
from django.core.files.base import ContentFile

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request

class CourseGenerationApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        aiModel = AiModel()

        response = aiModel.generateCourse(
            CourseRequestDto(1, request.data.get('courseName'), "practice", 2, 0))
        parsed_response = json.loads(response.text)
        newCourse = Course(
            name=parsed_response["courseTitle"],
            description=parsed_response["courseSummary"],
            cats_id=-1,
            author = request.user
        )
        newCourse.save()

        for chapter in parsed_response['chapters']:
            newLesson =  Lesson(course=newCourse,
                           name=chapter["chapterTitle"],
                           description=chapter["chapterSummary"], author=request.user)
            newLesson.save()

            for topic in chapter["topics"]:
                newMaterial = LessonContent(name=topic["topicTitle"],
                                        lesson=newLesson,
                                        content_type="text", author=request.user, is_teacher_only=False)
                newMaterial.content.save(gen_hash_name(topic["content"] + '.txt'),
                                     ContentFile(topic["content"]))
                newMaterial.save()

        return HttpResponse("OK", status=200)


    