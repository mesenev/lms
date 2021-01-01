from rest_framework import serializers

from course.models import Course, CourseSchedule
from users.serializers import DefaultUserSerializer


class CourseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=500)
    description = serializers.CharField()
    author = DefaultUserSerializer()

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        return Course.objects.create(**validated_data, **{'author': user})

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'author_id')


class ScheduleSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    class Meta:
        model = CourseSchedule
        fields = '__all__'
