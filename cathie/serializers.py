from rest_framework import serializers

from cathie.models import CatsAccount
from problem.models import Problem


class CatsProblemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Problem


class CatsAccountSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = CatsAccount
