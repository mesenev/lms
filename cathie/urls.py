from django.urls import path


from cathie import views

urlpatterns = [
    path('api/cats-problems/<int:course_id>/', views.get_cats_problems, name='cats-problems'),
    path(
        'api/cats-problem-description/<int:problem_id>/',
        views.get_cats_problem_description,
        name='cats-problem-description'
    ),
    path('api/cats-contests/', views.get_cats_contests, name='cats-contests'),
    path('api/add-users-to-contest/', views.add_users_to_contest, name='add-users-to-contest'),
    path('admin/cats/', views.cats_admin, name='cats-admin')
]
