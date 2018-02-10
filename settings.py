import os

import boto3


def here(*args):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *args)


PROJECT_ROOT = here('')


def project_root_joiner(*args):
    return os.path.join(os.path.abspath(PROJECT_ROOT), *args)


DEBUG = os.environ.get('DEBUG', True)
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 'A-random-and-secure-secret-key.\nKeep-this-very-SAFE!')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
)

STATIC_ROOT = project_root_joiner('', 'static/')
STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            project_root_joiner('', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug':
            DEBUG,
        },
    },
]

# dont specify a Database, we'll use dynamodb
# DATABASES = {}


UP_ENVIRONMENT = os.getenv("UP_ENVIRONMENT", None)

if UP_ENVIRONMENT:
    # this variables will be setup by CI,
    # during CI, we'll edit up.json and add this env vars
    DYNAMODB_SESSIONS_AWS_ACCESS_KEY_ID = os.getenv(
        "DYNAMODB_SESSIONS_AWS_ACCESS_KEY_ID")
    DYNAMODB_SESSIONS_AWS_SECRET_ACCESS_KEY = os.getenv(
        "DYNAMODB_SESSIONS_AWS_SECRET_ACCESS_KEY")
    DYNAMODB_SESSIONS_AWS_REGION_NAME = os.getenv(
        "DYNAMODB_SESSIONS_AWS_REGION_NAME", "eu-west-1")
else:
    DYNAMODB_SESSIONS_BOTO_SESSION = boto3.Session(
        profile_name='apex-up-profile')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s\n'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}
