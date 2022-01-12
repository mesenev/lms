from django.urls import path

from users import views

urlpatterns = [
    path('registration/', views.user_registration, name= 'account_registration'),
    path('login/', views.user_login, name='account_login'),
    path('logout/', views.Logout.as_view(), name='account_logout'),
    path('api/students_for_course/<int:course_id>/', views.students_for_course, name='students_for_course'),
    path('api/staff_for_course/<int:course_id>/', views.staff_for_course, name='staff_for_course'),
    path('api/change-password/', views.change_password, name='change_password'),
    path('api/change-avatar/', views.change_avatar, name='change_avatar'),
    path('api/teachersbymail/<int:course_id>/<str:email>/', views.find_teacher_by_email, name='find_teacher'),
    path('api/assignteacher/<int:course_id>/', views.assign_teacher, name='assign_teacher')
]
