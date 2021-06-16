from rest_framework import viewsets
from rest_framework import serializers

from rating.models import CourseProgress, LessonProgress, Attendance


class LessonProgressSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return LessonProgress.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.solved = validated_data.get('solved', instance.solved)
        instance.save()
        return instance

    class Meta:
        model = LessonProgress
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


class AttendanceSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Attendance.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.be = validated_data.get('be', instance.be)
        instance.save()
        return instance

    class Meta:
        model = Attendance
        fields = '__all__'
