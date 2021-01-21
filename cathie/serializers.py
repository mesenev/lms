from rest_framework import serializers

from problem.models import Problem


class CatsProblemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Problem
