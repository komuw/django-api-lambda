import uuid
import structlog

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.conf import settings
from django.http import HttpResponse


@api_view(('GET',))
def api_root(request):
    return Response({
        'Crawler': {
            'WorkerCrawler': reverse('WorkerCrawler', request=request),
        },
    })


def home_view(request):
    import sys
    logger = structlog.get_logger(__name__).bind(sessionId=str(uuid.uuid4()))

    logger.info("new_request", version=sys.version)
    return HttpResponse("<h1>Hello from django and up modules!</h1>")


DYNAMODB_CONN = settings.BOTO_SESSION.resource('dynamodb')
dynamoTable = DYNAMODB_CONN.Table('api-table')


class WorkerCrawler(APIView):
    """
    WorkerCrawler is triggered by dynamodb.

    """
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        """
        """
        logger = structlog.get_logger(__name__).bind(data=request.data)
        logger.info("worker_post_request_start")

        # process it
        logger.info("worker_post_request_end")
        return Response(status=status.HTTP_202_ACCEPTED)

    def get(self, request):
        """
        """
        logger = structlog.get_logger(__name__).bind(data=request.query_params.dict())
        logger.info("worker_get_request_start")

        # process it
        logger.info("worker_get_request_end")
        return Response(status=status.HTTP_202_ACCEPTED)
