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
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ussd.apps.UssdConfig',
)

STATIC_ROOT = project_root_joiner('', 'static/')
STATIC_URL = '/static/'


# dont specify a Database
# DATABASES = {}


SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

DEFAULT_USSD_SCREEN_JOURNEY = "ussd_journey.yaml"

DYNAMODB_SESSIONS_BOTO_SESSION = boto3.Session(profile_name='apex-up-profile')
DYNAMODB_SESSIONS_TABLE_NAME = "ussd-lambda-table"
SESSION_ENGINE = 'dynamoSessions'
# you can also use a cache backend to reduce hits to dynamoDB
# see: https://github.com/gtaylor/django-dynamodb-sessions/blob/master/dynamodb_sessions/backends/cached_dynamodb.py
