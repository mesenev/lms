from django.urls import path
from generate_study_materials import views

urlpatterns = [
    path('generate-course', views.CourseGenerationApi.as_view(), name='generate-course')
]