from django.conf.urls import url

from .views import resources, single_resource

urlpatterns = [
    url(r'^$', resources, name='all_resources'),
    url(r'^(?P<slug>[\w\-]+)/$', single_resource, {}, name='single_resource'),

]