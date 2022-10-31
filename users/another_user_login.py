from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.core.signing import Signer
from django.shortcuts import redirect
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from users.models import User
from users.serializers import DefaultUserSerializer
from users.utils import login_as_user, restore_original_login


@login_required
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def another_user_login(request):
    username = request.data.get('username')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response("Юзер не существует", status=404)
    if not request.user.is_superuser:
        return Response("Недостаточно прав", status=406)
    if user.is_superuser:
        return Response("Нельзя зайти за администратора", status=406)

    try:
        login_as_user(user, request)
    except ImproperlyConfigured:
        return redirect(request.META.get("HTTP_REFER", "/"))
    return redirect('index')


@login_required
@api_view(['GET'])
def another_user_logout(request):
    restore_original_login(request)
    return redirect('index')


@login_required
@api_view(['GET'])
def is_super_user(request):
    user = request.user
    if not user:
        return Response(status=404)
    return Response(user.is_superuser)


@login_required
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def session_user(request):
    signer = Signer()
    original_session = request.session.get(settings.USER_SESSION_FLAG)
    if original_session:
        original_user_pk = signer.unsign(original_session)
        try:
            user = User.objects.get(pk=original_user_pk)
            serialized_user = DefaultUserSerializer(user).data
            return Response(serialized_user)
        except User.DoesNotExist:
            return Response("Юзер не найден", status=404)
    else:
        return Response("Вы на основном аккаунте")

