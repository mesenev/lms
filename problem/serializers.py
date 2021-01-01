from rest_framework import serializers

from problem.models import Problem, Submit


class SubmitSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    class Meta:
        model = Submit
        fields = '__all__'


class ProblemSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    lesson = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    submits = SubmitSerializer(many=True)

    class Meta:
        model = Problem
        fields = ('id', 'name', 'description', 'author', 'lesson', 'submits')
