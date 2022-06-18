from django.core.files.base import ContentFile
from rest_framework import serializers

from lesson.models import Lesson, LessonContent
from problem.serializers import ProblemSerializer
from problem.storages import gen_hash_name
from rating.serializers import LessonProgressSerializer
from users.serializers import DefaultUserSerializer


class MaterialSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    lesson = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all())
    author = DefaultUserSerializer(required=False, read_only=True)
    name = serializers.CharField()
    content_type = serializers.CharField(allow_blank=True)
    content = serializers.CharField()

    def _change_content(self, content):
        with self.instance.content.open("w") as temp:
            temp.write(content)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.content = validated_data.get('content', instance.content)

        if validated_data.get('content'):
            self._change_content(validated_data.get('content'))

        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request and hasattr(request, 'user') else None
        content = validated_data.get('content')
        validated_data.pop('content')
        lesson = LessonContent.objects.create(**validated_data, **{'author': user})
        lesson.content.save(gen_hash_name(content) + '.txt', ContentFile(content), save=True)
        return lesson

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance is not None:
            rep["content"] = self._get_file_content(instance)
        return rep

    @staticmethod
    def _get_file_content(instance):
        if not instance.content.name:
            return ""

        with instance.content.file.open() as temp:
            return temp.read()

    class Meta:
        model = LessonContent
        fields = ('id', 'lesson', 'content_type', 'author', 'content')


class LessonShortSerializer(serializers.ModelSerializer):
    problems = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'deadline', 'problems', 'is_hidden', 'scores']


class LessonSerializer(serializers.ModelSerializer):
    problems = ProblemSerializer(many=True, read_only=True)
    materials = MaterialSerializer(many=True, read_only=True)
    progress = LessonProgressSerializer(many=True, read_only=True)

    def create(self, validated_data):
        if 'materials' in validated_data:
            del validated_data["materials"]
        if 'problems' in validated_data:
            del validated_data["problems"]
        if 'progress' in validated_data:
            del validated_data["progress"]
        request = self.context.get("request")
        user = request.user if request and hasattr(request, 'user') else None
        validated_data['scores'] = {'CW': 50, 'HW': 50, 'EX': 10}
        if 'author' in validated_data:
            del validated_data["author"]
        return Lesson.objects.create(**validated_data, **{'author': user})

    class Meta:
        model = Lesson
        fields = '__all__'
