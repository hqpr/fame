from django.conf.urls import include, url
from django.contrib import admin

from .views import blogs, single_blog

urlpatterns = [
    # Examples:

    url(r'^$', blogs, name='all_blogs'),
    url(r'^(?P<slug>[\w\-]+)/$', single_blog, {}, name='single_blog'),

]