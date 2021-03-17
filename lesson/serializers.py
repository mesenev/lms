from rest_framework import serializers

from lesson.models import Lesson, LessonContent, LessonProgress
from users.serializers import DefaultUserSerializer


class MaterialSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    lesson = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all())
    author = DefaultUserSerializer(required=False, read_only=True)
    name = serializers.CharField()
    content_type = serializers.CharField(allow_blank=True)
    content = serializers.CharField()

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.content = validated_data.get('content', instance.content)
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


class LessonSerializer(serializers.ModelSerializer):

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

# class LessonShortSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Lesson
#         fields = '__all__'
