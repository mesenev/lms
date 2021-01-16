from rest_framework import serializers

from cathie.models import CatsProblem


class CatsProblemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = CatsProblem
