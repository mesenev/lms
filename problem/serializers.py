from rest_framework import serializers
from users.serializers import DefaultUserSerializer
from problem.models import Problem, Submit


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
    author = DefaultUserSerializer(required=False, read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    submits = SubmitSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
         instance.name = validated_data.get('name', instance.name)
         instance.description = validated_data.get('description', instance.description)
         instance.author = validated_data.get('author', instance.author)
         instance.save()
         return instance

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request and hasattr(request, "user") else None
        return Problem.objects.create(**validated_data, **{'author': user})

    class Meta:
        model = Problem
        fields = ('id', 'name', 'description', 'author', 'lesson', 'submits')
