from django.conf.urls import include, url, patterns
from .views import AudioView, AudioFileView, PlayListView

urlpatterns = [
    url(r'^audio/add_1/$', AudioFileView.as_view(), name='add_audio_step1'),
    url(r'^audio/add_2/(?P<object_id>\d+)/$', AudioView.as_view(), name='add_audio_step2'),
    url(r'^playlist/add/$', PlayListView.as_view(), name='add_playlist'),
]

