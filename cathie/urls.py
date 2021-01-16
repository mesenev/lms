from django.urls import path

from cathie import views

urlpatterns = [
    path('cats-problems/<id>/', views.get_cats_problems, name='cats-problems'),
]
