from rest_framework import serializers

from problem.models import Problem, Submit
from users.serializers import DefaultUserSerializer


class SubmitSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    problem = serializers.PrimaryKeyRelatedField(read_only=True)
    student = DefaultUserSerializer(read_only=True)
    content = serializers.CharField()
    status = serializers.CharField()

    def update(self, instance, validated_data):
        print(validated_data)
        instance.content = validated_data.get('content', instance.content)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    def create(self, validated_data):
        request = self.context.get('request')
        student = request.user if request and hasattr(request, 'user') else None
        problem = request.problem if request and hasattr(request, 'problem') else (
            Problem.objects.last()
        )
        return Submit.objects.create(**validated_data, **{
            'student': student,
            'problem': problem
        })

    class Meta:
        model = Submit


class ProblemSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    lesson = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    submits = SubmitSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    class Meta:
        model = Problem
        fields = ('id', 'name', 'description', 'author', 'lesson', 'submits')
