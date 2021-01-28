from rest_framework import serializers

from course.models import Course
from lesson.models import Lesson, LessonContent, LessonProgress
from problem.serializers import ProblemSerializer
from users.serializers import DefaultUserSerializer
from users.models import User


class MaterialSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    lesson = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all())
    author = DefaultUserSerializer(required=False, read_only=True)
    name = serializers.CharField()
    content_type = serializers.CharField(allow_blank=True)
    content = serializers.CharField()

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.content = validated_data.get('description', instance.content)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request and hasattr(request, 'user') else None
        return LessonContent.objects.create(**validated_data, **{'author': user})

    class Meta:
        model = LessonContent
        fields = ('id', 'lesson', 'content_type', 'author', 'content')


class LessonProgressSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    lesson = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all())
    solved = serializers.CharField(max_length=1024)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def create(self, validated_data):
        return LessonProgress.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.solved = validated_data.get('solved', instance.solved)
        instance.save()
        return instance

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=500)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    description = serializers.CharField()
    author = DefaultUserSerializer(required=False, read_only=True)
    problems = ProblemSerializer(many=True, required=False, default=list())
    materials = MaterialSerializer(many=True, required=False, default=list())
    deadline = serializers.DateField()
    progress = LessonProgressSerializer(many=True, required=False, default=list())

    def create(self, validated_data):
        del validated_data["materials"]
        del validated_data["problems"]
        del validated_data["progress"]
        request = self.context.get("request")
        user = request.user if request and hasattr(request, 'user') else None
        return Lesson.objects.create(**validated_data, **{'author': user})

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.author = validated_data.get('author', instance.author)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        instance.save()
        return instance

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'description', 'author_id')
