from django.conf.urls import url

from apps.artist.views import artists, single_artist

urlpatterns = [
    # Examples:
    # url(r'^$', 'fame.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', artists, name='all_artists'),
    url(r'^(?P<slug>[\w\-]+)/$', single_artist, {"display":"overview"}, name='single_artist'),
    url(r'^(?P<slug>[\w\-]+)/(?P<type>[\w\-]+)/$', single_artist, {"display":"type"}, name='single_artist'),
    url(r'^(?P<slug>[\w\-]+)/(?P<type>[\w\-]+)/(?P<type_id>[\w\-]+)/$', single_artist, {"display":"type_id"}, name='single_artist'),
]
