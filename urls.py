from django.conf.urls import url

import views


urlpatterns = (
    url(r'^$', views.api_root, name='api-root'),
    url(r'^staging/crawler/?$', views.WebCrawler.as_view(), name='webcrawler'),
)
