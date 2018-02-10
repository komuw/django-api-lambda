import uuid
import structlog

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import HttpResponse

import tasks


@api_view(('GET',))
def api_root(request):
    return Response({
        'Crawler': {
            'WebCrawler': reverse('webcrawler', request=request),
        },
    })


def home_view(request):
    import sys
    logger = structlog.get_logger(__name__).bind(sessionId=str(uuid.uuid4()))

    logger.info("new_request", version=sys.version)
    return HttpResponse("<h1>Hello from django and up modules!</h1>")


class WebCrawler(APIView):
    """
    WebCrawler is a Web Crawler as a service.

    This view accepts requests from customers. Customers call this view with
    id: a unique id to identify this request
    target: the particular url that  they would like to crawl
    callback: the url on their service that we should post(callback) results of our scraping to.

    {
        "id": "uniqueID",
        "target": "http://www.google.com",
        "callback": "http://www.example.com/callback"
    }
    """
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        """
        Return a list of all users.
        """
        logger = structlog.get_logger(__name__).bind(id=request.data['id'])
        logger.info("request_start", data=request.data)

        status_code = tasks.crawl(data=request.data)
        tasks.callback(status_code, request.data)

        return Response(status=status.HTTP_202_ACCEPTED)
