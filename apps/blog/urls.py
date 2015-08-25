from django.conf.urls import url

from apps.blog.views import blogs, single_blog

urlpatterns = [
    # Examples:

    url(r'^$', blogs, name='all_blogs'),
    url(r'^(?P<slug>[\w\-]+)/$', single_blog, {}, name='single_blog'),

]