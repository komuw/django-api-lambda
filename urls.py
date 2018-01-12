from django.conf.urls import url

from views import home_view, ExampeUssd


urlpatterns = (
    url(r'^$', home_view),
    url(r'^ussd/?', ExampeUssd.as_view(), name='ussd_app')
)


# curl -X POST -H "Content-Type: application/json" \
#      -d '{"phoneNumber": "400","sessionId": "105","text":"1", "serviceCode": "312"}' \
#      "http://127.0.0.1:43804/ussd"
