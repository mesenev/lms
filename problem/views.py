import django_filters
from django.db import models
from django.db.models import Q, Prefetch, Subquery
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, exceptions, status, permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from course.models import Course
from lesson.models import Lesson
from problem.models import Problem, Submit, CatsSubmit, ProblemStats, LogEvent
from problem.serializers import ProblemSerializer, SubmitSerializer, SubmitListSerializer, ProblemListSerializer, \
    LogEventSerializer, LastSubmitSerializer
from users.models import User
from users.permissions import CourseStaffOrReadOnlyForStudents, object_to_course, \
    CourseStaffOrAuthor


class ProblemViewSet(viewsets.ModelViewSet):
    # TODO: check only opened lessons are distributed for students
    permission_classes = [CourseStaffOrReadOnlyForStudents]

    filterset_fields = ['lesson_id', ]

    def get_queryset(self):
        queryset = Problem.objects.filter(
            Q(lesson__course__in=self.request.user.staff_for.all())
            | (Q(
                lesson__course__in=self.request.user.student_for.all(),
                lesson__is_hidden=False
            ))
        )
        return queryset

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

    @staticmethod
    def prefetch_query_with_submits(request: Request, queryset):
        submits = request.user.submits.annotate(
            ordering=models.Case(
                models.When(status="OK", then=models.Value(0)),
                models.When(status="AW", then=models.Value(1)),
                default=models.Value(2),
                output_field=models.IntegerField()
            )
        ).order_by('problem', 'ordering', '-id').distinct('problem')
        return queryset.prefetch_related(models.Prefetch(lookup='submits', to_attr='last_submit', queryset=submits))

    @action(detail=False, url_path='by-course/(?P<course_id>\d+)')
    def by_course(self, request, course_id):
        queryset = self.get_queryset().filter(
            lesson__course=course_id,
            lesson__is_hidden=False,
        ).exclude(
            submits__in=Submit.objects.filter(
                Q(student=request.user)
                & Q(status__in=[Submit.AWAITING_MANUAL, Submit.OK, Submit.DEFAULT_STATUS])
            )
        )

        queryset = self.prefetch_query_with_submits(request, queryset)
        serializer = ProblemListSerializer(list(queryset)[:5], many=True)

        return Response(serializer.data)

    @action(detail=False, url_path='user-submit')
    def get_problem_list_for_user(self, request):
        queryset = self.prefetch_query_with_submits(request, self.filter_queryset(self.get_queryset()))
        serializer = ProblemListSerializer(queryset, many=True)
        return Response(serializer.data)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 1000


class SubmitFilter(django_filters.FilterSet):
    course = django_filters.ModelChoiceFilter(
        label='course', queryset=Course.objects.all(), method='course_filter'
    )
    lesson = django_filters.ModelChoiceFilter(
        label='lesson', queryset=Lesson.objects.all(), method='lesson_filter'
    )
    problem = django_filters.ModelChoiceFilter(
        label='problem', queryset=Lesson.objects.all(), method='problem_filter'
    )

    class Meta:
        model = Submit
        fields = ['problem', 'student', 'status', 'cats_submit__is_sent', ]

    def course_filter(self, queryset, name, value):
        return queryset.filter(lesson__course=value)

    def lesson_filter(self, queryset, name, value):
        return queryset.filter(**{f'problem__{name}': value})

    def problem_filter(self, queryset, name, value):
        return queryset.filter(problem=value)


class SubmitViewSet(viewsets.ModelViewSet):
    permission_classes = [CourseStaffOrReadOnlyForStudents]
    serializer_class = SubmitSerializer
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
        return queryset

    @action(detail=False, url_path='cats-result/(?P<submit_id>\d+)')
    def cats_result(self, request, submit_id):
        queryset = self.get_queryset().filter(id=submit_id).all()
        if not queryset.exists():
            raise exceptions.NotFound
        return Response(queryset.first().cats_submit.first().testing_result)

    @action(detail=False, url_path='five-aw/(?P<course_id>\d+)', permission_classes=[CourseStaffOrAuthor])
    def five_aw(self, request, course_id):
        queryset = self.get_queryset().filter(
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

    @action(detail=False, url_path=r'last-user-submit/(?P<user_id>[^/.]+)/(?P<problem_id>[^/.]+)')
    def get_last_user_problem_submit(self, request, user_id, problem_id):
        return Response(LastSubmitSerializer(
            Submit.objects.filter(problem__id=problem_id, student__id=user_id).annotate(
                ordering=self.stats_ordering).order_by('problem', 'ordering', '-id').first()
        ).data)

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
            if 'status' in request.data:
                del request.data['status']
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

        if validated_data['problem'].test_mode == 'manual':
            model = serializer.save(student=request.user, status=Submit.DEFAULT_STATUS)
            log_event = LogEvent(
                problem=validated_data['problem'], student=request.user, type=LogEvent.TYPE_AWAITING_MANUAL,
                submit=model,
                data=dict(message='Решение ожидает ручной проверки')
            )
            log_event.save()
            return

        cats = CatsSubmit(data=dict(
            source_text=validated_data.get('content'),
            problem_id=validated_data['problem'].cats_id,
            contest_id=Course.objects.filter(
                lessons__problems__id=validated_data['problem'].id
            ).first().cats_id,
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
        if 'content' in serializer.initial_data:
            del serializer.initial_data['content']
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


class LogEventsPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 1000


class LogEventViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = LogEvent.objects.all()
    serializer_class = LogEventSerializer
    filterset_class = LogEventFilter
    pagination_class = LogEventsPagination
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        user = self.request.user
        queryset = LogEvent.objects.filter(
            Q(problem__lesson__course__in=user.staff_for.all())
            | Q(problem__lesson__course__in=user.student_for.all())
        )
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.initial_data['author'] = request.user.id
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
