from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from apps.api_rest.views import audio_like, audio_comment, playlists, playlist, profile_details, user_status, user_connect,\
                   list_artists, audio, video, video_like, video_comment, \
                   list_competitions, chart_list, chart_list_fame, chart_update, competition_entry_rating, all_media,\
                   conversations, single_conversation, message, connections

urlpatterns = [
    # Artists
    url(r'^artists/$', list_artists, name="list_artists"),
    url(r'^status/$', user_status, name="user_status"),
    url(r'^details/$', profile_details, name="profile_details"),
    url(r'^connect/$', user_connect, name="user_connect"),
    url(r'^connect/(?P<user_id>[0-9]+)$', user_connect, name="user_connect"),

    # Competitions
    url(r'^competitions/$', list_competitions, name="list_competitions"),
    url(r'^competitions/(?P<competition_slug>[\w\-]+)/chart$', chart_list, name="chart_list"),
    url(r'^competitions/(?P<competition_slug>[\w\-]+)/chart/update$', chart_update, name="chart_update"),
    url(r'^competitions/(?P<competition_slug>[\w\-]+)/(?P<competition_entry_id>[0-9]+)/rate$', competition_entry_rating, name="competition_entry_rating"),

    # Media
    url(r'^chart$', chart_list_fame, name="chart_list_fame"),
    url(r'^media$', all_media, name="api_all_media"),
    url(r'^media/(?P<media_type>[\w\-]+)$', all_media, name="api_all_media"),
    url(r'^audio/(?P<audio_id>[0-9]+)$', audio, name="api_audio"),
    url(r'^audio/like$', audio_like, name="audio_like"),
    url(r'^audio/comment$', audio_comment, name="audio_comment"),
    url(r'^playlists$', playlists, name="playlists"),
    url(r'^playlist/(?P<playlist_id>[0-9]+)$', playlist, name="api_playlist"),
    url(r'^video/(?P<video_id>[0-9]+)$$', video, name="api_video"),
    url(r'^video/like$', video_like, name="video_like"),
    url(r'^video/comment$', video_comment, name="video_comment"),

    # Messaging
    url(r'^conversations/$', conversations, name="api_conversation"),
    url(r'^conversations/(?P<pk>[0-9]+)/$', single_conversation, name="api_single_conversation"),
    url(r'^messages/(?P<pk>[0-9]+)/$', message, name="api_message"),
    url(r'^connections/$', connections, name="api_connections"),

    # url(r'^snippets/(?P<pk>[0-9]+)$', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)