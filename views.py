import uuid
import structlog

from django.http import HttpResponse

from ussd.core import UssdView, UssdRequest


def home_view(request):
    import sys
    logger = structlog.get_logger(__name__).bind(sessionId=str(uuid.uuid4()))

    logger.info("new_request", version=sys.version)
    return HttpResponse("<h1>Hello from django and up modules!</h1>")


class ExampeUssd(UssdView):
    customer_journey_conf = "ussd_journey.yaml"
    customer_journey_namespace = "example_namespace"

    def post(self, req):
        session_id = req.data["sessionId"]
        msisdn = req.data["phoneNumber"].strip("+")
        user_input = req.data["text"]

        logger = structlog.get_logger(__name__).bind(sessionId=session_id)
        logger.info("new_ussd_request",
                    msisdn=msisdn,
                    user_input=user_input)

        return UssdRequest(
            phone_number=msisdn,
            session_id=session_id,
            ussd_input=user_input,
            service_code=req.data.get("serviceCode", ""),
            language=req.data.get("language", "en")
        )

    def ussd_response_handler(self, ussd_response):
        if ussd_response.status:
            res = "CON" + " " + str(ussd_response)
            response = HttpResponse(res)
        else:
            res = "END" + " " + str(ussd_response)
            response = HttpResponse(res)
        return response
