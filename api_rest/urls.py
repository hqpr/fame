from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import audio_like, audio_comment, playlists, playlist, profile_details, user_status, user_connect

urlpatterns = [
    url(r'^audio/like$', audio_like, name="audio_like"),
    url(r'^audio/comment$', audio_comment, name="audio_comment"),
    url(r'^playlists$', playlists, name="playlists"),
    url(r'^playlist/(?P<playlist_id>[0-9]+)$', playlist, name="playlist"),
    url(r'^details/$', profile_details, name="profile_details"),
    url(r'^status/$', user_status, name="user_status"),
    url(r'^connect/$', user_connect, name="user_connect"),
    url(r'^connect/(?P<user_id>[0-9]+)$', user_connect, name="user_connect"),
    # url(r'^snippets/(?P<pk>[0-9]+)$', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)