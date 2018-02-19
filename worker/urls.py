from django.conf.urls import url

import views


urlpatterns = (
    # url(r'^$', views.api_root, name='api-root'),
     url(r'^$', views.WorkerCrawler.as_view(), name='WorkerCrawler'),
)
