from rest_framework import serializers

from lesson.models import Lesson
from problem.models import Problem, Submit, ProblemStats, LogEvent
from users.serializers import DefaultUserSerializer


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
        return Submit.objects.create(**validated_data)

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


class ProblemStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemStats
        fields = ('green', 'red', 'yellow')


class LogEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEvent
        fields = '__all__'


class ProblemListSerializer(serializers.ModelSerializer):
    last_submit = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()

    def get_last_submit(self, instance):
        if hasattr(instance, 'last_submit') and len(instance.last_submit) > 0:
            return SubmitListSerializer(instance.last_submit[0]).data
        else:
            return None

    def get_stats(self, instance):
        if hasattr(instance, 'stats') and instance.stats:
            return ProblemStatsSerializer(instance.stats).data
        return None

    class Meta:
        model = Problem
        fields = (
            'id', 'name', 'last_submit', 'lesson', 'type', 'stats'
        )


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
    de_options = serializers.SerializerMethodField()

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
            'id', 'name', 'description', 'author', 'lesson', 'submits',
            'manual', 'type', 'language', 'cats_material_url', 'cats_id', 'students',
            'de_options'
        )
