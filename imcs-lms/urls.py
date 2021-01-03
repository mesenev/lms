from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from course.views import CourseViewSet
from lesson.views import LessonViewSet
from problem.views import ProblemViewSet, SubmitViewSet
from users.views import index

router = DefaultRouter()
router.register('course', CourseViewSet, basename='course')
router.register('lesson', LessonViewSet, basename='lesson')
router.register('problem', ProblemViewSet, basename='problem')
router.register('submit', SubmitViewSet, basename='submit')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    re_path(r"^.*$", index),
]
