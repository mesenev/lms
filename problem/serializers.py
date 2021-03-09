from rest_framework import serializers

from lesson.models import Lesson
from problem.models import Problem, Submit
from users.serializers import DefaultUserSerializer


class SubmitSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    problem = serializers.PrimaryKeyRelatedField(queryset=Problem.objects.all())
    content = serializers.CharField()
    status = serializers.ChoiceField(choices=Submit.SUBMIT_STATUS, default='NP', required=False)
    student = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)

    def update(self, instance, validated_data):
        print(validated_data)
        instance.content = validated_data.get('content', instance.content)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    def create(self, validated_data):
        return Submit.objects.create(**validated_data)

    class Meta:
        model = Submit
        fields = ['id', 'problem', 'student', 'content', 'status', ]


class ProblemSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    lesson = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all())
    author = DefaultUserSerializer(required=False, read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    submits = SubmitSerializer(many=True, read_only=True)
    manual = serializers.BooleanField()
    type = serializers.CharField()
    language = serializers.CharField(required=True, allow_null=True)
    cats_material_url = serializers.CharField()
    students = serializers.SerializerMethodField()

    def get_students(self, instance):
        return {student.id: student.submits.values('id', 'status', 'student').all().first()
                for student in instance.students.all()}

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request and hasattr(request, "user") else None
        return Problem.objects.create(**validated_data, **{'author': user})

    class Meta:
        model = Problem
        fields = (
            'id', 'name', 'description', 'author', 'lesson', 'submits',
            'manual', 'type', 'language', 'cats_material_url', 'cats_id', 'students'
        )
