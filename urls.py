from django.conf.urls import url, include

import views


urlpatterns = (
    url(r'^root/?$', include('rest_framework.urls')),
    url(r'^process/?$', views.MyApi.as_view()),
)
