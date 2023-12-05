import random
import string

from rest_framework import serializers

from course.models import Course, CourseSchedule, CourseLink
from lesson.serializers import LessonShortSerializer
from users.models import GroupAssignStudent
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
    cats_id = serializers.IntegerField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    schedule = serializers.PrimaryKeyRelatedField(
        read_only=True, required=False
    )

    def validate_author(self, value):
        return

    def create(self, validated_data):
        if hasattr(validated_data, 'lessons'):
            del validated_data['lessons']
        request = self.context.get("request")
        user = request.user if request and hasattr(request, "user") else None
        instance = Course.objects.create(**validated_data, **{'author': user})
        CourseSchedule.objects.create(course_id=instance.id, lessons=[], week_schedule={}, start_date=None)
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.author = validated_data.get('author', instance.author)
        instance.cats_id = validated_data.get('cats_id', instance.cats_id)
        instance.de_options = validated_data.get('de_options', instance.de_options)
        instance.save()
        return instance

    def validate(self, attrs):
        return super(CourseSerializer, self).validate(attrs)
        # todo validate cats_id

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'author', 'lessons',
                  'cats_id', 'schedule', 'de_options']


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSchedule
        fields = '__all__'


class LinkSerializer(serializers.Serializer):
    # TODO: cleanup this serializer
    id = serializers.ReadOnlyField()
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    link = serializers.SerializerMethodField(required=False)
    usages = serializers.IntegerField()

    @staticmethod
    def get_link(instance):
        return instance.link

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return CourseLink.objects.create(**validated_data, link=''.join(
            random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(15)))

    class Meta:
        model = CourseLink
        fields = '__all__'


class AssignTeacherSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    id = serializers.IntegerField(required=True)
