from django.conf.urls import url, include

import views


urlpatterns = (
    url(r'^$', views.api_root, name='api-root'),
    url(r'^api-auth/', include('rest_framework.urls'), name='browsable_api'),
    url(r'^crawler/?$', views.WebCrawler.as_view(), name='webcrawler'),
)
