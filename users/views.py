from django.http import HttpResponse

from django.shortcuts import render

# Create your views here.
from users.models import Person


def my_first_view(request):
    p: Person = Person.objects.filter(first_name__contains='123')
    a = Person()
    a.first_name = '123'
    a.last_name = 'last'
    a.save()
    return HttpResponse(f'name: {p.first_name}, surname: {p.last_name}')
