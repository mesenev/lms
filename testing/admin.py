from django.contrib import admin
from testing.models import TestingProblem, TestingSubmit, TestingQueue, InProgressTesting

admin.site.register(TestingProblem)
admin.site.register(TestingSubmit)
admin.site.register(TestingQueue)
admin.site.register(InProgressTesting)