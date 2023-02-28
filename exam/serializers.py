from rest_framework import serializers
from exam.models import ExaminationForm, ExamSolution, Question
from django_pydantic_field import SchemaField


class ExamSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField()

    class Meta:
        model = ExaminationForm
        fields = '__all__'


class ExamSolutionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField()

    class Meta:
        model = ExamSolution
        fields = '__all__'
