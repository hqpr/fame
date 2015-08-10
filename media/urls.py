from django.conf.urls import include, url, patterns
from .views import AudioView, AudioFileView, PlayListView, trackcard, AudioUpdateView, \
    playlist_cover, VideoFileView, VideoView, videocard, all_media, all_tracks, all_videos, all_playlists, add_to_playlist, playlistcard,\
    PlayListUpdateView, publisher, soundcloud_import, share

urlpatterns = [
    url(r'^$', all_media, name='all_media'),
    url(r'^tracks/$', all_tracks, name='all_tracks'),
    url(r'^videos/$', all_videos, name='all_videos'),
    url(r'^playlists/$', all_playlists, name='all_playlists'),
    url(r'^audio/add_1/$', AudioFileView.as_view(), name='add_audio_step1'),
    url(r'^audio/add_2/(?P<object_id>\d+)/$', AudioView.as_view(), name='add_audio_step2'),

    url(r'^video/add_1/$', VideoFileView.as_view(), name='add_video_step1'),
    url(r'^video/add_2/(?P<object_id>\d+)/$', VideoView.as_view(), name='add_video_step2'),

    url(r'^playlist/add/$', PlayListView.as_view(), name='add_playlist'),
    url(r'^playlist/addtrack/(?P<track_id>\d+)/$', add_to_playlist, name='add_to_playlist'),
    url(r'^audio/edit/(?P<object_id>\d+)/$', AudioUpdateView.as_view(), name='edit_audio'),
    url(r'^video/edit/(?P<object_id>\d+)/$', VideoView.as_view(), name='edit_video'),
    url(r'^playlist/edit/(?P<object_id>\d+)/$', PlayListUpdateView.as_view(), name='edit_playlist'),
    url(r'^trackcard/(?P<track_id>\d+)/$', trackcard, name='trackcard'),
    url(r'^videocard/(?P<video_id>\d+)/$', videocard, name='videocard'),
    url(r'^playlistcard/(?P<playlist_id>\d+)/$', playlistcard, name='playlistcard'),
    url(r'^share/(?P<uid>\w+)/$', share, name='share'),

    # image upload
    url(r'^playlist/cover/$', playlist_cover, name='playlist_cover'),

    url(r'^publisher/$', publisher, name='publisher'),
    url(r'^soundcloud/import/$', soundcloud_import, name='soundcloud_import'),
]

