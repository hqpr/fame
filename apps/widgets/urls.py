from django.conf.urls import url

from apps.widgets.views import trackcard

urlpatterns = [
    url(r'^trackcard/(?P<uid>\w+)/$', trackcard, name='widget_trackcard'),
]

