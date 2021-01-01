from rest_framework.routers import DefaultRouter

from course.views import CourseViewSet

router = DefaultRouter()
router.register('course', CourseViewSet, basename='course')

