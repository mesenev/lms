from rest_framework import viewsets
from testing.models import TestingProblem, TestingSubmit
from testing.serializers import TestingProblemSerializer, TestingSubmitSerializer

class TestingProblemViewSet(viewsets.ModelViewSet):
    queryset = TestingProblem.objects.all()
    serializer_class = TestingProblemSerializer

class TestingSubmitViewSet(viewsets.ModelViewSet):
    queryset = TestingSubmit.objects.all()
    serializer_class = TestingSubmitSerializer