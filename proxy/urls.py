from django.conf.urls import url
from .views import proxy_view

app_name = 'proxy'
urlpatterns = [
    url(r'^(?P<url>.*)$', proxy_view, name='proxy_view'),
]
