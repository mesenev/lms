from django.conf import settings as django_settings
from django.contrib.auth import load_backend
from django.contrib.auth import login
from django.contrib.auth import logout
from imcslms import settings as loc_settings
from django.core.exceptions import ImproperlyConfigured
from users.models import User
from django.core.signing import SignatureExpired
from django.core.signing import Signer

signer = Signer()


def login_as_user(user, request, store_original_user=True):
    original_user = request.user

    if not hasattr(user, "backend"):
        for backend in django_settings.AUTHENTICATION_BACKENDS:
            if not hasattr(load_backend(backend), "get_user"):
                continue

            if user == load_backend(backend).get_user(user.pk):
                user.backend = backend
                break
        else:
            raise ImproperlyConfigured(
                "Could not find an appropriate authentication backend"
            )

    if not hasattr(user, "backend"):
        return

    login(request, user)

    if store_original_user:
        request.session[loc_settings.USER_SESSION_FLAG] = signer.sign(original_user.pk)


def restore_original_login(request):
    original_session = request.session.get(loc_settings.USER_SESSION_FLAG)
    logout(request)

    if not original_session:
        return

    try:
        original_user_pk = signer.unsign(original_session)
        user = User.objects.get(pk=original_user_pk)
    except User.DoesNotExist:
        return

    try:
        original_user_pk = signer.unsign(original_session)
        user = User.objects.get(pk=original_user_pk)
        login_as_user(user, request, store_original_user=False)
        if loc_settings.USER_SESSION_FLAG in request.session:
            del request.session[loc_settings.USER_SESSION_FLAG]
    except SignatureExpired:
        pass
