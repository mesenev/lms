from django.urls import path

from users import views

urlpatterns = [
    path('api/students_for_course/<int:course_id>/', views.students_for_course, name='students_for_course'),
    path('api/staff_for_course/<int:course_id>/', views.staff_for_course, name='staff_for_course'),
]
