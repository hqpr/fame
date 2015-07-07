from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import audio_like, audio_comment, playlists, playlist

urlpatterns = [
    url(r'^audio/like$', audio_like),
    url(r'^audio/comment$', audio_comment),
    url(r'^playlists$', playlists),
    url(r'^playlist/(?P<playlist_id>[0-9]+)$', playlist),
    # url(r'^snippets/(?P<pk>[0-9]+)$', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)