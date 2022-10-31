from rest_framework import serializers

from rating.models import CourseProgress, LessonProgress


class LessonProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonProgress
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ('attendance', 'lesson', 'id')


class CourseProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseProgress
        fields = ('course', 'progress', 'user',)
