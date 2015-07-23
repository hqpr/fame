from django.conf.urls import include, url, patterns
from .views import back, drop_ls, youtube_view, imageupload, mixcl, sound

urlpatterns = [
    url(r'^to/(.*)/$', back, name='connector'),
    url(r'^dropbox/metadata/$', drop_ls, name='drop'),

    url(r'^my/youtube/$', youtube_view, name='youtube_console'),

    url(r'^imageupload/$', imageupload, name='imageupload'),

    url(r'^my/mixcloud/$', mixcl, name='mixcl'),
    url(r'^test/$', sound, name='sound'),


]

