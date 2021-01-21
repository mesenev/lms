from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from course.views import CourseViewSet
from lesson.views import LessonViewSet, MaterialViewSet
from problem.views import ProblemViewSet, SubmitViewSet
from users.views import index, user_login, UsersViewSet

router = DefaultRouter()
router.register('course', CourseViewSet, basename='course')
router.register('lesson', LessonViewSet, basename='lesson')
router.register('problem', ProblemViewSet, basename='problem')
router.register('submit', SubmitViewSet, basename='submit')
router.register('material', MaterialViewSet, basename='material')
router.register('users', UsersViewSet, basename='users')

urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_DIR)
urlpatterns += [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('cathie.urls')),
    path('', include('users.urls')),
    path('', include('problem.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', user_login, name='account_login'),
    re_path(r"^.*$", index, name='index'),
]
