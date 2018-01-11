from django.conf.urls import url

from .views import home_view

urlpatterns = (
    url(r'^$', home_view),
    # Your other preferred django urls can be added here.
)
