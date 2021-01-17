from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from cathie.cats_api import cats_get_problems_from_contest
from course.models import Course


@login_required
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_cats_problems(request, course_id):
    course = Course.objects.get(pk=course_id)
    cats_problems = cats_get_problems_from_contest(course.cats_id, request.user)
    return Response(cats_problems)
