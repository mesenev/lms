from django.urls import path

from lesson import views

urlpatterns = [
    path('api/delete-lesson/<int:id>/', views.delete_lesson, name='delete-lesson')
]
