from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path, reverse_lazy
from rest_framework.routers import DefaultRouter
from django.views.generic.base import RedirectView

from cathie.views import CatsAccountViewSet
from course.views import CourseViewSet, ScheduleViewSet
from lesson.views import LessonViewSet, MaterialViewSet, AttachmentViewSet
from problem.views import ProblemViewSet, SubmitViewSet, LogEventViewSet
from rating.views import LessonProgressViewSet, CourseProgressViewSet
from users.views import index, UsersViewSet
from exam.views import ExamViewSet, ExamSolutionViewSet
from group.views import CourseGroupViewSet, CourseGroupLinkViewSet

router = DefaultRouter()
router.register('course', CourseViewSet, basename='course')
router.register('course-schedule', ScheduleViewSet, basename='schedule')
router.register('lesson', LessonViewSet, basename='lesson')
router.register('problem', ProblemViewSet, basename='problem')
router.register('submit', SubmitViewSet, basename='submit')
router.register('material', MaterialViewSet, basename='material')
router.register('attachments', AttachmentViewSet, basename='attachments')
router.register('users', UsersViewSet, basename='users')
router.register('lessonprogress', LessonProgressViewSet, basename='lessonprogress')
router.register('courseprogress', CourseProgressViewSet, basename='courseprogress')
router.register('grouplink', CourseGroupLinkViewSet, basename='grouplink')
router.register('logevents', LogEventViewSet, basename='logevent')
router.register('cats_account', CatsAccountViewSet, basename='cats_account')
router.register('exam', ExamViewSet, basename='exam')
router.register('solution', ExamSolutionViewSet, basename='exam_solution')
router.register('group', CourseGroupViewSet, basename='group')

urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# import debug_toolbar
# urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]

urlpatterns += [
    path('admin', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    path('admin/', admin.site.urls),
    path('', include('cathie.urls')),
    path('', include('users.urls')),
    path('', include('lesson.urls')),
    path('', include('problem.urls')),
    path('', include('group.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    re_path(r"^.*$", index, name='index'),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ]