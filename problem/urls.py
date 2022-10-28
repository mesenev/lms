from django.urls import path

from problem import views

urlpatterns = [
    path('api/add-cats-problems-to-lesson/<int:lesson_id>/', views.add_cats_problems, name='add-cats-problems')
]
