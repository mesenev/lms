from django.urls import path

from problem import views

urlpatterns = [
    path('api/add-cats-problems-to-lesson/<int:lesson_id>/', views.add_cats_problems, name='add-cats-problems'),
    path('api/get-last-user-problem-submit/<int:user_id>/<int:problem_id>/', views.get_last_user_problem_submit, name='get-last-user-problem-submit')
]
