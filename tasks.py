from __future__ import absolute_import, unicode_literals

import json

import requests
from celery import shared_task
from structlog import get_logger


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


@shared_task(bind=True, name='crawl')
def crawl(self, data):
    """
    """
    logger = get_logger(__name__).bind(id=data['id'])
    logger.info('crawl_task_start', data=data)
    r = requests.get(data['target'], timeout=3)
    logger.info('crawl_task_end', status=r.status_code)

    return r.status_code


@shared_task(bind=True, name='callback')
def callback(self, status_code, data):
    """
    """
    logger = get_logger(__name__).bind(id=data['id'])
    logger.info('callback_task_start', data=data)

    callback_data = {
        "id": data['id'],
        "status_code": status_code
    }
    r = requests.post(
        data['callback'],
        data=json.dumps(callback_data),
        timeout=3)

    logger.info(
        'callback_task_end',
        status=r.status_code,
        callback_data=callback_data)
