from rest_framework import serializers

from lesson.models import Lesson, LessonContent, Attachment
from problem.serializers import ProblemSerializer
from rating.serializers import LessonProgressSerializer
from users.serializers import DefaultUserSerializer
from exam.serializers import ExamSerializer


class AttachmentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        attachment = Attachment.objects.create(**validated_data)
        attachment.save()
        return attachment

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.material = validated_data.get('material', instance.material)
        instance.file_url = validated_data.get('file_url', instance.file_url)
        instance.file_format = validated_data.get('file_format', instance.file_format)
        instance.save()
        return instance

    class Meta:
        model = Attachment
        fields = ('id', 'name', 'material', 'file_url', 'file_format')


class MaterialSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    lesson = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all())
    author = DefaultUserSerializer(required=False, read_only=True)
    name = serializers.CharField()
    content_type = serializers.CharField(allow_blank=True)
    content = serializers.CharField()
    is_teacher_only = serializers.BooleanField()

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.content = validated_data.get('content', instance.content)
        instance.author = validated_data.get('author', instance.author)
        instance.is_teacher_only = validated_data.get('is_teacher_only', instance.is_teacher_only)
        instance.content_type = validated_data.get('content_type', instance.content_type)
        instance.save()
        return instance

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request and hasattr(request, 'user') else None
        return LessonContent.objects.create(**validated_data, **{'author': user})

    class Meta:
        model = LessonContent
        fields = ('id', 'lesson', 'content_type', 'author', 'content', 'is_teacher_only')


class LessonShortSerializer(serializers.ModelSerializer):
    problems = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'deadline', 'problems', 'is_hidden', 'scores']


class LessonSerializer(serializers.ModelSerializer):
    problems = ProblemSerializer(many=True, read_only=True)
    materials = MaterialSerializer(many=True, read_only=True)
    progress = LessonProgressSerializer(many=True, read_only=True)
    exams = ExamSerializer(many=True, read_only=True)

    def create(self, validated_data):
        if 'materials' in validated_data:
            del validated_data["materials"]
        if 'problems' in validated_data:
            del validated_data["problems"]
        if 'progress' in validated_data:
            del validated_data["progress"]
        if 'exams' in validated_data:
            del validated_data["exams"]
        request = self.context.get("request")
        user = request.user if request and hasattr(request, 'user') else None
        validated_data['scores'] = {'CW': 50, 'HW': 50, 'EX': 10}
        if 'author' in validated_data:
            del validated_data["author"]
        return Lesson.objects.create(**validated_data, **{'author': user})

    class Meta:
        model = Lesson
        fields = '__all__'


class AddCatsProblemSerializer(serializers.Serializer):
    problem_data = serializers.JSONField(required=True)
    problem_type = serializers.IntegerField(required=True)
