from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from django.conf import settings  # noqa: F401


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

app = Celery('apps')


app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(
)  # app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
