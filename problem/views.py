import django_filters
from django.db import models
from django.db.models import Q, Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, exceptions, status
from rest_framework.decorators import api_view, renderer_classes, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from cathie.cats_api import cats_get_problem_description_by_url
from course.models import Course
from lesson.models import Lesson
from problem.models import Problem, Submit, CatsSubmit, ProblemStats, LogEvent
from problem.serializers import ProblemSerializer, SubmitSerializer, SubmitListSerializer, ProblemListSerializer, \
    LogEventSerializer
from users.models import User
from users.permissions import CourseStaffOrReadOnlyForStudents, object_to_course, CourseStaffOrAuthorReadOnly


class ProblemViewSet(viewsets.ModelViewSet):
    permission_classes = [CourseStaffOrReadOnlyForStudents]
    queryset = Problem.objects.all()
    filterset_fields = ['lesson_id', ]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProblemListSerializer
        return ProblemSerializer

    def list(self, request, *args, **kwargs):
        stats_query = ProblemStats.objects.filter(problem__lesson__course__staff=request.user)
        queryset = self.filter_queryset(self.get_queryset().prefetch_related(
            Prefetch(lookup='problemstats', to_attr='stats', queryset=stats_query)
        ))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='by-course/(?P<course_id>\d+)')
    def by_course(self, request, course_id):
        submits = request.user.submits.annotate(
            ordering=models.Case(
                models.When(status="OK", then=models.Value(0)),
                models.When(status="AW", then=models.Value(1)),
                default=models.Value(2),
                output_field=models.IntegerField()
            )
        ).order_by('problem', 'ordering', '-id').distinct('problem')
        queryset = self.queryset.filter(
            lesson__course=course_id
        ).exclude(
            lesson__is_hidden=True,
            submits__status__in=[
                Submit.AWAITING_MANUAL,
                Submit.OK,
                Submit.DEFAULT_STATUS
            ]
        ).prefetch_related(models.Prefetch(lookup='submits', to_attr='last_submit', queryset=submits))
        serializer = ProblemListSerializer(list(queryset)[:5], many=True)

        return Response(serializer.data)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000


class SubmitFilter(django_filters.FilterSet):
    course = django_filters.ModelChoiceFilter(
        label='course', queryset=Course.objects.all(), method='course_filter'
    )
    lesson = django_filters.ModelChoiceFilter(
        label='lesson', queryset=Lesson.objects.all(), method='lesson_filter'
    )

    class Meta:
        model = Submit
        fields = ['problem', 'student', 'status', 'cats_submit__is_sent', ]

    def course_filter(self, queryset, name, value):
        queryset = queryset.filter(lesson__course=value)
        return queryset

    def lesson_filter(self, queryset, name, value):
        queryset = queryset.filter(**{f'problem__{name}': value})
        return queryset


class SubmitViewSet(viewsets.ModelViewSet):
    permission_classes = [CourseStaffOrReadOnlyForStudents]
    serializer_class = SubmitSerializer
    queryset = Submit.objects.prefetch_related('cats_submit').all()
    pagination_class = StandardResultsSetPagination
    filterset_class = SubmitFilter
    stats_ordering = models.Case(
        models.When(status=Submit.OK, then=models.Value(0)),
        models.When(status=Submit.AWAITING_MANUAL, then=models.Value(1)),
        default=models.Value(2),
        output_field=models.IntegerField()
    )

    def get_queryset(self):
        user = self.request.user
        queryset = Submit.objects.filter(
            Q(student=user) | Q(problem__lesson__course__in=user.staff_for.all())
        ).prefetch_related('problem')
        problem_id = self.request.query_params.get('', None)
        user_id = self.request.query_params.get('', None)
        course_id = self.request.query_params.get('', None)
        lesson_id = self.request.query_params.get('', None)
        if course_id:
            queryset = queryset.filter(lesson__course__id=course_id)
        if lesson_id:
            queryset = queryset.filter(lesson__course__id=lesson_id)

        if problem_id:
            user = User.objects.get(pk=user_id) if user_id else None
            is_staff = True if user and user.is_staff else False
            if is_staff:
                return queryset.filter(problem__id=problem_id)
            elif user:
                return queryset.filter(problem__id=problem_id, student__id=user_id)

        return queryset

    @action(detail=False, url_path='five-aw/(?P<course_id>\d+)')
    def five_aw(self, request, course_id):
        # TODO: check permissions for it
        queryset = Submit.objects.filter(
            problem__lesson__course__id=course_id
        ).annotate(
            ordering=self.stats_ordering
        ).prefetch_related(
            'problem'
        ).order_by(
            'student', 'problem', 'ordering', '-id'
        ).distinct('student', 'problem')
        # filtering over distinct leads to ignoring distinct oO
        # that's why I have to filter manually gg

        serializer = SubmitListSerializer(list(filter(
            lambda x: x.status == Submit.AWAITING_MANUAL,
            queryset
        ))[:5], many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='problem-stats/(?P<problem_id>\d+)')
    def problem_stats(self, request, problem_id):
        # TODO: check permissions for it
        queryset = Submit.objects.filter(
            problem__id=problem_id
        ).annotate(
            ordering=self.stats_ordering
        ).order_by('student', 'ordering', '-id').distinct('student')
        serializer = SubmitListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request: Request, *args, **kwargs):
        problem = Problem.objects.get(id=request.data['problem'])
        course = object_to_course(problem)
        if request.user.assigns.filter(course=course).exists():
            return super().create(request, *args, **kwargs)
        elif course in list(request.user.staff_for.all()) + list(request.user.author_for.all()):
            return super().create(request, *args, **kwargs)
        raise exceptions.PermissionDenied

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubmitListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = SubmitListSerializer(queryset, many=True)
        return Response(serializer.data)

    # def create_cats_submit_by_submit(self, submit: Submit):
    def perform_create(self, serializer):
        request = serializer.context["request"]
        validated_data = serializer.validated_data
        # TODO: Change it according to prefs of problem
        if not validated_data['problem'].cats_id:
            return
        cats = CatsSubmit(data=dict(
            source_text=validated_data.get('content'),
            problem_id=validated_data['problem'].cats_id,
            de_id=validated_data.get('de_id'),
            # source=validated_data.get('source'),
        ))
        model = serializer.save(student=request.user, status=Submit.DEFAULT_STATUS)
        cats.submit = model
        cats.save()
        return

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.initial_data["updated_by"] = request.user.id
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class LogEventFilter(django_filters.FilterSet):
    problem = django_filters.ModelChoiceFilter(label='problem', queryset=Problem.objects.all())
    student = django_filters.ModelChoiceFilter(label='student', queryset=User.objects.all())

    class Meta:
        model = LogEvent
        fields = ['student', 'problem']

    def problem_filter(self, queryset, name, value):
        queryset = queryset.filter(problem=value)
        return queryset

    def student_filter(self, queryset, name, value):
        queryset = queryset.filter(student=value)
        return queryset


class LogEventViewSet(viewsets.ModelViewSet):
    permission_classes = [CourseStaffOrAuthorReadOnly]
    queryset = LogEvent.objects.all()
    serializer_class = LogEventSerializer
    filterset_class = LogEventFilter
    filter_backends = (DjangoFilterBackend,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.initial_data['author'] = request.user.id
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def add_cats_problems(request, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    if lesson.course not in list(request.user.staff_for.all()) + list(request.user.author_for.all()):
        raise exceptions.PermissionDenied
    data = request.data
    answer = list()
    for cats_problem in data:
        materials = cats_get_problem_description_by_url(cats_problem["text_url"])
        problem = Problem.objects.create(
            lesson=lesson, author=request.user, name=cats_problem['name'],
            cats_id=cats_problem['id'], cats_material_url=cats_problem["text_url"],
            description=materials,
        )
        answer.append(ProblemSerializer(problem).data)
    return Response(answer)
