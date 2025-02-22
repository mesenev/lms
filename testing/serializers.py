from rest_framework import serializers
from testing.models import TestingProblem, TestingSubmit

class TestingProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestingProblem
        fields = '__all__'


class TestingSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestingSubmit
        fields = '__all__'