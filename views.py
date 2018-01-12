import uuid
import structlog

from django.http import HttpResponse

# setup views


def home_view(request):
    logger = structlog.get_logger(__name__).bind(sessionId=str(uuid.uuid4()))

    logger.info('new_request', name='komu', age=45)
    return HttpResponse('<h1>Hello from django and up modules!</h1>')
