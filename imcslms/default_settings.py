import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'helloworld'
DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'users',
    'course',
    'lesson',
    'problem',
    'cathie',
    'celery_app',
    'rating',
    'channels',
    'wsnotifications',
]

REST_FRAMEWORK = dict(
    DEFAULT_FILTER_BACKENDS=['django_filters.rest_framework.DjangoFilterBackend'],
    DATE_INPUT_FORMATS=["%d/%m/%Y", "%Y-%m-%d"],
    DATE_FORMAT="%d/%m/%Y",
    DEFAULT_PERMISSION_CLASSES=['rest_framework.permissions.IsAuthenticated']
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'imcslms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'imcslms.wsgi.application'
ASGI_APPLICATION = 'imcslms.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379')],
        },
    },
}

DATABASES = {'default':
    {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': 'database',
        'PORT': os.getenv('DATABASE_PORT', '5432'),
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
STATICFILES_DIRS = ['frontend/dist', ]
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = 'media'

WEBPACK_DEV_SERVER = 'localhost:8080/static/'
AUTH_USER_MODEL = 'users.User'
CATS_URL = os.getenv('CATS_URL', '')
CATS_LOGIN = os.getenv('CATS_LOGIN', '')
CATS_PASSWD = os.getenv('CATS_PASSWD', '')

# Celery Configuration Options
CELERY_TIMEZONE = 'Asia/Vladivostok'
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
