from django.urls import path

from group import views

urlpatterns = [
    path('api/check-link/<str:link>/', views.CheckLinkApi.as_view(), name='check-link'),
    path('api/delete-link/<str:link>/', views.LinkDeletionAPi.as_view(), name='delete-link'),
    path('api/group-registration/<str:link>/', views.GroupRegistrationApi.as_view(), name='course-registration'),
]
