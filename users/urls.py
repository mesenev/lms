from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users import views

urlpatterns = [
    path('logout/', views.Logout.as_view(), name='account_logout'),
    path('api/students_for_course/<int:course_id>/', views.students_for_course, name='students_for_course'),
    path('api/staff_for_course/<int:course_id>/', views.staff_for_course, name='staff_for_course'),
    path('api/change-password/', views.change_password, name='change_password'),
    path('api/change-avatar/', views.change_avatar, name='change_avatar'),
    path('api/edit-profile/', views.edit_profile, name='edit_profile'),
    path('api/teachersbymail/<int:course_id>/<str:email>/', views.find_teacher_by_email, name='find_teacher'),
    path('api/assignteacher/<int:course_id>/', views.assign_teacher, name='assign_teacher'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('api/data_of_user/', views.data_user, name='data_user'),
]
