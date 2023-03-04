from rest_framework import viewsets, exceptions
from users.permissions import CourseStaffOrAuthorReadOnly, CourseStaffOrReadOnlyForStudents
from exam.models import ExaminationForm, ExamSolution, AnswerTypes
from django.db.models import Q
from imcslms.default_settings import TEACHER
from exam.serializers import ExamSerializer, ExamSolutionSerializer
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response


class AddAttachmentToQuestion(APIView):

    def post(self, request: Request):
        pass


class ExamViewSet(viewsets.ModelViewSet):
    serializer_class = ExamSerializer
    permission_classes = [CourseStaffOrReadOnlyForStudents]
    filterset_fields = ['lesson_id', ]

    def get_queryset(self):
        user = self.request.user
        return ExaminationForm.objects.all()\
            .filter(
            (Q(is_hidden=False) & Q(lesson__course__in=user.student_for.all()))
            | Q(lesson__course__in=user.staff_for.all())
            | Q(lesson__course__in=user.author_for.all())
        )

    def create(self, request, *args, **kwargs):
        if request.user.groups.filter(name=TEACHER).exists():
            return super().create(request, *args, **kwargs)
        raise exceptions.PermissionDenied


class ExamSolutionViewSet(viewsets.ModelViewSet):
    serializer_class = ExamSolutionSerializer
    permission_classes = [CourseStaffOrAuthorReadOnly]
    filterset_fields = ['exam', 'student']

    def get_queryset(self):
        user = self.request.user
        return ExamSolution.objects.all().filter(
            Q(exam__lesson__course__in=user.staff_for.all())
            | Q(exam__lesson__course__in=user.author_for.all()) | Q(student=user)
        )

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        request = serializer.context['request']
        validated_data = serializer.validated_data

        questions = validated_data['exam'].questions
        question_answers = validated_data['user_answers']
        current_score = 0
        correct_questions = []
        for answer in question_answers:
            current_question = questions[answer['question_index']]
            if validated_data['exam'].test_mode == 'auto_and_manual' and \
                    (current_question['answer_type'] == AnswerTypes.text or current_question['answer_type'] ==
                     AnswerTypes.input):
                continue
            if set(map(lambda ans: (ans.strip()).lower(),  answer['submitted_answers'])) ==\
                    set(map(lambda ans: (ans.strip()).lower(), current_question['correct_answers'])):
                current_score += questions[answer['question_index']]['points']
                correct_questions.append(answer['question_index'])

        if validated_data['exam'].test_mode == 'manual' or validated_data['exam'].test_mode == 'auto_and_manual':
            serializer.save(student=request.user, status=ExamSolution.SOLUTION_STATUS[0][1], score=0)
            return

        serializer.save(student=request.user, status=ExamSolution.SOLUTION_STATUS[1][1], score=current_score,
                        correct_questions_indexes=correct_questions)
        return

    def update(self, request, *args, **kwargs):
        request_data = request.data
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)