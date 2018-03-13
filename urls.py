from django.conf.urls import url

from . import views


urlpatterns = (
    url(r'^$', views.api_root, name='api-root'),
    # in lambda, this uri will be available under /staging/crawler
    url(r'^crawler/?$', views.WebCrawler.as_view(), name='webcrawler'),
)
