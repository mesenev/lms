from rest_framework import serializers

from course.models import Course, CourseSchedule, CourseLink
from lesson.serializers import LessonSerializer
from users.models import CourseAssignTeacher
from users.serializers import DefaultUserSerializer


class CourseSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    author = DefaultUserSerializer(required=False, read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    students = DefaultUserSerializer(many=True, required=False, read_only=True)

    def validate_author(self, value):
        return

    def create(self, validated_data):
        if hasattr(validated_data, 'lessons'):
            del validated_data['lessons']
        request = self.context.get("request")
        user = request.user if request and hasattr(request, "user") else None
        instance = Course.objects.create(**validated_data, **{'author': user})
        CourseAssignTeacher.objects.create(user=user, course=instance)
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'author', 'lessons', 'students']


class ScheduleSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    class Meta:
        model = CourseSchedule
        fields = '__all__'

class LinkSerializer(serializers.Serializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    link = serializers.CharField()
    usages = serializers.IntegerField()

    #TODO: get usages be positive nums only (1...)
    #update and create funcs
    #POST -> generate a link
    #GET <- give a link

    def update(self, instance, validated_data):
            pass

    def create(self, validated_data):
        pass

    class Meta:
         model = CourseLink
         fields = '__all__'