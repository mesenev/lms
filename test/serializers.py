from rest_framework import serializers
from test.models import Test, TestSolution
from django.db import models
from lesson.models import Lesson


class TestSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField()

    class Meta:
        model = Test
        fields = '__all__'


class TestSolutionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField()

    class Meta:
        model = TestSolution
        fields = '__all__'
