import os


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

DATABASES = {
    'default': {
        'ENGINE':
        'django.db.backends.postgresql',
        'NAME':
        'ryiafstd',
        'USER':
        'ryiafstd',
        'PASSWORD':
        'zVrRQGR5Vd8h1695jnNkYi4LFPdZauLt',
        'HOST':
        'horton.elephantsql.com',
        'PORT':
        '5432',
    }
}

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

DEFAULT_USSD_SCREEN_JOURNEY = "ussd_journey.yaml"
