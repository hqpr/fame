from django.conf.urls import include, url, patterns
from .views import AudioView, AudioFileView, PlayListView, trackcard, AudioUpdateView, \
    playlist_cover

urlpatterns = [
    url(r'^audio/add_1/$', AudioFileView.as_view(), name='add_audio_step1'),
    url(r'^audio/add_2/(?P<object_id>\d+)/$', AudioView.as_view(), name='add_audio_step2'),
    url(r'^playlist/add/$', PlayListView.as_view(), name='add_playlist'),
    url(r'^audio/edit/(?P<object_id>\d+)/$', AudioUpdateView.as_view(), name='edit_audio'),
    url(r'^trackcard/(?P<track_id>\d+)/$', trackcard, name='trackcard'),

    # image upload
    url(r'^playlist/cover/$', playlist_cover, name='playlist_cover'),
]

