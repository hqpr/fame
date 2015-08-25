from django.conf import settings
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from apps.artist.views import single_artist, artist_settings, connections
from .views import hall_of_fame, search, terms, partnerships, handler404, handler4042, home


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    # Examples:
    url(r'^$', home, name='home'),
    # url(r'^blog/', include('blog.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^sitepanel/', include(admin.site.urls)),
    url(r'^competitions/', include('apps.competition.urls')),
    url(r'^artists/', include('apps.artist.urls')),

    url(r'^connect/', include('apps.socialconnector.urls')),
    url(r'^media/', include('apps.media.urls')),
    url(r'^blog/', include('apps.blog.urls')),

    #  userprofile
    url(r'^user/', include('apps.userprofile.urls')),

    # api
    url(r'^api/', include('apps.api_rest.urls')),

    # static pages
    url(r'^profile/$', login_required(single_artist), {"display": "profile"}, name="profile"),
    url(r'^profile/connections$', login_required(connections), {"display": "profile"}, name="connections"),
    url(r'^settings/$', login_required(artist_settings), {"display":"profile"}, name="settings"),

    # static pages - phase 2
    url(r'^faq/$', 'apps.content.views.faq', {}, name="faq"),
    url(r'^hall-of-fame/$', hall_of_fame, {}, name="hall_of_fame"),
    url(r'^search/$', search, {}, name="search"),
    url(r'^terms-and-conditions/$', terms, {}, name="terms"),
    url(r'^partnerships/$', partnerships, {}, name="partnerships"),
    url(r'^404/$', handler404, {}, name="handler404"),
    url(r'^404-2/$', handler4042, {}, name="handler404_2"),

    url(r'^insights/', include('apps.insights.urls')),
    url(r'^widget/', include('apps.widgets.urls')),
    url(r'^subscribe/', include('apps.subscription.urls')),
    url(r'^home/', include('apps.home.urls')),
    url(r'^messages/', include('apps.messaging.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
                            url(r'^rosetta/', include('rosetta.urls')),
                            )