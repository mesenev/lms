from django.urls import path

from course import views

urlpatterns = [
    path('api/check-link/<str:link>/', views.check_link, name='check-link'),
    path('api/course-registration/<str:link>/', views.course_registration, name='course-registration'),
]
