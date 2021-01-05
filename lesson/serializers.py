from rest_framework import serializers

from course.models import Course
from lesson.models import Lesson
from problem.serializers import ProblemSerializer
from users.serializers import DefaultUserSerializer


class LessonSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=500)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    description = serializers.CharField()
    author = DefaultUserSerializer(required=False, read_only=True)
    problems = ProblemSerializer(many=True, required=False, default=list())

    def create(self, validated_data):
        del validated_data["problems"]
        request = self.context.get("request")
        user = request.user if request and hasattr(request, "user") else None
        return Lesson.objects.create(**validated_data, **{'author': user})

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'description', 'author_id')
