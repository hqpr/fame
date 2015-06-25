from django.conf.urls import include, url, patterns
from .views import back, drop_ls, youtube_view, create_playlist, \
    add_to_playlist, imageupload, insta, mixcl

urlpatterns = [
    url(r'^to/(.*)/$', back, name='connector'),
    url(r'^dropbox/metadata/$', drop_ls, name='drop'),

    # url(r'^my/photo/$', PhotoView.as_view(), name='upload_photo'),
    # url(r'^my/sound/$', AudioView.as_view(), name='upload_sound'),
    # url(r'^my/video/$', VideoView.as_view(), name='upload_video'),
    url(r'^my/youtube/$', youtube_view, name='youtube_console'),

    url(r'^my/video/playlist/$', create_playlist, name='create_playlist'),
    url(r'^my/video/playlist/add/$', add_to_playlist, name='add_to_playlist'),

    url(r'^imageupload/$', imageupload, name='imageupload'),

    url(r'^my/instagram/$', insta, name='insta'),
    url(r'^my/mixcloud/$', mixcl, name='mixcl'),

]

