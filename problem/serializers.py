from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from lesson.models import Lesson
from problem.models import Problem, Submit, ProblemStats, LogEvent
from users.serializers import DefaultUserSerializer
from lesson.storages import gen_hash_name
from django.core.files.base import ContentFile

class CatsResultField:
    pass


class SubmitSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    problem = serializers.PrimaryKeyRelatedField(queryset=Problem.objects.all())
    content = serializers.CharField()
    updated_at = serializers.ReadOnlyField()
    status = serializers.ChoiceField(choices=Submit.SUBMIT_STATUS, default='NP', required=False)
    student = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)

    def update(self, instance, validated_data):
        update_fields = list(
            x for x in ['status', 'updated_by'] if x in validated_data
            and validated_data.get(x) != getattr(instance, x)
        )
        instance.status = validated_data.get('status', instance.status)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.save(update_fields=update_fields)
        return instance

    def create(self, validated_data):
        content = validated_data.get('content')
        validated_data.pop('content')
        submit = Submit.objects.create(**validated_data)
        print('CREATE!!!!!!!!!!!!!!!!!')
        submit.content.save(gen_hash_name(content) + '.txt', ContentFile(content), save=True)
        return submit

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
        model = Submit
        fields = [
            'id', 'problem', 'student', 'content', 'status', 'de_id', 'updated_at', 'updated_by',
        ]


class SubmitListSerializer(serializers.ModelSerializer):
    problem = serializers.SerializerMethodField()
    lesson = serializers.SerializerMethodField()

    def get_problem(self, instance):
        return dict(id=instance.problem.id, name=instance.problem.name)

    def get_lesson(self, instance):
        return instance.problem.lesson_id

    class Meta:
        model = Submit
        fields = ['id', 'problem', 'student', 'status', 'created_at', 'lesson', ]


class LastSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submit
        fields = ['id', 'status']


class ProblemStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemStats
        fields = ('green', 'red', 'yellow')


class LogEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEvent
        fields = '__all__'

    def validate(self, attrs):
        super(LogEventSerializer, self).validate(attrs)
        if attrs.get("type") and not attrs.get("data").get("message"):
            raise ValidationError(detail='Message cannot be empty', code=status.HTTP_400_BAD_REQUEST)
        return attrs


class ProblemListSerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField()
    last_submit = serializers.SerializerMethodField()

    def get_stats(self, instance):
        if hasattr(instance, 'stats') and instance.stats:
            return ProblemStatsSerializer(instance.stats).data
        return None

    def get_last_submit(self, instance):
        if hasattr(instance, 'last_submit') and instance.last_submit:
            return LastSubmitSerializer(instance.last_submit).data
        return None

    class Meta:
        model = Problem
        fields = (
            'id', 'name', 'lesson', 'type', 'stats', 'last_submit'
        )


class ProblemSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    lesson = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all())
    author = DefaultUserSerializer(required=False, read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    submits = SubmitSerializer(many=True, read_only=True)
    stats = serializers.SerializerMethodField(read_only=True)
    manual = serializers.BooleanField()
    type = serializers.CharField()
    language = serializers.CharField(required=True, allow_null=True)
    cats_material_url = serializers.CharField()
    students = serializers.SerializerMethodField()
    de_options = serializers.SerializerMethodField()
    test_mode = serializers.CharField()

    def get_stats(self, instance):
        if hasattr(instance, 'problemstats') and instance.problemstats:
            return ProblemStatsSerializer(instance.problemstats).data
        return None

    def get_students(self, instance):
        return {student.id: student.submits.values('id', 'status', 'student').all().first()
                for student in instance.students.all()}

    def get_de_options(self, instance):
        return instance.de_options or instance.lesson.course.de_options

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request and hasattr(request, "user") else None
        return Problem.objects.create(**validated_data, **{'author': user})

    class Meta:
        model = Problem
        fields = (
            'id', 'name', 'description', 'author', 'lesson', 'submits', 'stats',
            'manual', 'type', 'language', 'cats_material_url', 'cats_id', 'students',
            'de_options', 'test_mode'
        )
