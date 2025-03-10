from django.urls import path, include
from users import another_user_login as as_another_user_views
from users import views

urlpatterns = [
    path('api/anotheruserlogin', as_another_user_views.another_user_login, name='another_user_login'),
    path('api/anotheruserlogout', as_another_user_views.another_user_logout, name='another_user_logout'),
    path('api/sessionuser', as_another_user_views.session_user, name='session_user'),
    path('api/issuperuser', as_another_user_views.is_super_user, name='is_super_user'),
    path('api/change-avatar/', views.changeAvatar.as_view(), name='change_avatar'),
    path('api/password_reset/request_token', views.RequestTokenAPIView.as_view(),
         name="reset_password_token_request"),
    path('api/password_reset/with_token', views.ChangePasswordWithTokenAPIView.as_view(),
         name="password_reset_with_token"),
    path('api/password_reset/verify_token', views.VerifyTokenExists.as_view(),
         name="verify_token_exists"),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/auth/', include('djoser.urls.authtoken')),

]
