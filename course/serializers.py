import random
import string

from rest_framework import serializers

from course.models import Course, CourseSchedule, CourseLink, CourseProgress
from lesson.serializers import LessonSerializer, LessonShortSerializer
from users.models import CourseAssignTeacher
from users.serializers import DefaultUserSerializer
from utils.dynamic_fields_serializer import DynamicFieldsModelSerializer


class CourseShortSerializer(serializers.ModelSerializer):
    author = DefaultUserSerializer(required=False, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'author']


class CourseSerializer(DynamicFieldsModelSerializer):
    id = serializers.ReadOnlyField()
    author = DefaultUserSerializer(required=False, read_only=True)
    lessons = LessonShortSerializer(many=True, read_only=True)
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
        fields = ['id', 'name', 'description', 'author', 'lessons', 'students', 'staff']


class ScheduleSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    class Meta:
        model = CourseSchedule
        fields = '__all__'


class LinkSerializer(serializers.Serializer):
    # TODO: cleanup this serializer
    id = serializers.ReadOnlyField()
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    link = serializers.SerializerMethodField(required=False)
    usages = serializers.IntegerField()

    def get_link(self, instance):
        return instance.link

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return CourseLink.objects.create(**validated_data, link=''.join(
            random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(15)))

    class Meta:
        model = CourseLink
        fields = '__all__'


class CourseProgressSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return CourseProgress.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.lessons = validated_data.get('lessons', instance.lessons)
        instance.attendance = validated_data.get('attendance', instance.attendance)
        instance.save()
        return instance

    class Meta:
        model = CourseProgress
        fields = '__all__'
