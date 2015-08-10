from django.conf.urls import include, url, patterns
from .views import trackcard

urlpatterns = [
    url(r'^trackcard/(?P<uid>\w+)/$', trackcard, name='widget_trackcard'),
]

