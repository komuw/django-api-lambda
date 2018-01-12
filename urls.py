from django.conf.urls import url

from views import home_view

from ussd.views import AfricasTalkingUssdGateway

urlpatterns = (
    url(r'^$', home_view),
    url(r'^ussd/?', AfricasTalkingUssdGateway.as_view(), name='ussd_app')
)
