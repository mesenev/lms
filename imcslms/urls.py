import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from course.models import CourseSchedule
from course.views import CourseViewSet, LinkViewSet, ScheduleViewSet
from lesson.views import LessonViewSet, MaterialViewSet
from problem.views import ProblemViewSet, SubmitViewSet
from rating.views import LessonProgressViewSet, CourseProgressViewSet
from users.views import index, UsersViewSet

router = DefaultRouter()
router.register('course', CourseViewSet, basename='course')
router.register('course-schedule', ScheduleViewSet, basename='schedule')
router.register('lesson', LessonViewSet, basename='lesson')
router.register('problem', ProblemViewSet, basename='problem')
router.register('submit', SubmitViewSet, basename='submit')
router.register('material', MaterialViewSet, basename='material')
router.register('users', UsersViewSet, basename='users')
router.register('lessonprogress', LessonProgressViewSet, basename='lessonprogress')
router.register('courseprogress', CourseProgressViewSet, basename='courseprogress')
router.register('courselink', LinkViewSet, basename='courselink')

urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]
urlpatterns += [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('cathie.urls')),
    path('', include('users.urls')),
    path('', include('problem.urls')),
    path('', include('course.urls')),
    path('api-auth/', include('rest_framework.urls')),
    re_path(r"^.*$", index, name='index'),
]

