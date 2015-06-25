from django.conf import settings
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from .views import login, register
from artist.views import single_artist, artist_settings, artist_insights

urlpatterns = [
    # Examples:
    # url(r'^$', 'fame.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),

    url(r'^sitepanel/', include(admin.site.urls)),
    url(r'^competitions/', include('competition.urls')),
    url(r'^artists/', include('artist.urls')),

    url(r'^connect/', include('socialconnector.urls')),
    url(r'^media/', include('media.urls')),

    # static pages
    url(r'^login/$', login, name="login"),
    url(r'^register/$', register, name="register"),
    url(r'^profile/$', login_required(single_artist), {"display":"profile"}, name="profile"),
    url(r'^profile/insights/$', artist_insights, {"display":"profile"}, name="insights"),
    url(r'^settings/$', artist_settings, {"display":"profile"}, name="settings"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)