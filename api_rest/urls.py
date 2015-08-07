from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import audio_like, audio_comment, playlists, playlist, profile_details, user_status, user_connect,\
                   list_artists, audio, video, video_like, video_comment, \
                   list_competitions

urlpatterns = [
    # Artists
    url(r'^artists/$', list_artists, name="list_artists"),
    url(r'^status/$', user_status, name="user_status"),
    url(r'^details/$', profile_details, name="profile_details"),
    url(r'^connect/$', user_connect, name="user_connect"),
    url(r'^connect/(?P<user_id>[0-9]+)$', user_connect, name="user_connect"),

    # Competitions
    url(r'^competitions/$', list_competitions, name="list_competitions"),

    # Media
    url(r'^audio/(?P<audio_id>[0-9]+)$$', audio, name="api_audio"),
    url(r'^audio/like$', audio_like, name="audio_like"),
    url(r'^audio/comment$', audio_comment, name="audio_comment"),
    url(r'^playlists$', playlists, name="playlists"),
    url(r'^playlist/(?P<playlist_id>[0-9]+)$', playlist, name="playlist"),
    url(r'^video/(?P<video_id>[0-9]+)$$', video, name="api_video"),
    url(r'^video/like$', video_like, name="video_like"),
    url(r'^video/comment$', video_comment, name="video_comment"),
    # url(r'^snippets/(?P<pk>[0-9]+)$', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)