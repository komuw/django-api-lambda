import os

# setup settings
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
    'ussd.apps.UssdConfig',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

DEFAULT_USSD_SCREEN_JOURNEY = "ussd_journey.yaml"
