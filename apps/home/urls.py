from django.conf.urls import url

from .views import home, complete_tutorial

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^complete/tutorial/$', complete_tutorial, name='complete_tutorial'),
]

