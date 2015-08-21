from django.conf.urls import url
from .views import messages, conversation


urlpatterns = [
    url(r'^$', messages, name='messages'),
    url(r'^(?P<pk>[0-9]+)/$', conversation, name='conversation'),
]

