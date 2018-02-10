from __future__ import absolute_import, unicode_literals

from structlog import get_logger
from celery import shared_task


# The @shared_task decorator lets you create tasks without having any
# concrete app instance:
@shared_task(bind=True, name='add')
def add(self, x, y):
    """
    You can call it as: add.delay(23, 56)
    """
    logger = get_logger(__name__)
    logger.info('add_task_start')
    z = x + y
    logger.info('add_task_end')
    return z
       