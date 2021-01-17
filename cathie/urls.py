from django.urls import path

from cathie import views

urlpatterns = [
    path('api/cats-problems/<int:course_id>/', views.get_cats_problems, name='cats-problems'),
]
