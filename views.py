import uuid
import structlog

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


from django.http import HttpResponse


def home_view(request):
    import sys
    logger = structlog.get_logger(__name__).bind(sessionId=str(uuid.uuid4()))

    logger.info("new_request", version=sys.version)
    return HttpResponse("<h1>Hello from django and up modules!</h1>")


class MyApi(APIView):
    """
    """
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        """
        Return a list of all users.
        """
        req_data = request.data
        return Response(status=status.HTTP_202_ACCEPTED)
