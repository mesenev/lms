from rest_framework import serializers

from course.models import Course, CourseSchedule
from lesson.serializers import LessonSerializer
from users.serializers import DefaultUserSerializer


class CourseSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    author = DefaultUserSerializer(required=False, read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    def validate_author(self, value):
        return

    def create(self, validated_data):
        if hasattr(validated_data, 'lessons'):
            del validated_data['lessons']
        request = self.context.get("request")
        user = request.user if request and hasattr(request, "user") else None
        return Course.objects.create(**validated_data, **{'author': user})

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'author', 'lessons']


class ScheduleSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    class Meta:
        model = CourseSchedule
        fields = '__all__'
