from django.conf.urls import url

from views import home_view, ExampeUssd


urlpatterns = (
    url(r'^$', home_view),
    url(r'^ussd/?', ExampeUssd.as_view(), name='ussd_app')
)
