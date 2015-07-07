from django.conf import settings
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from artist.views import single_artist, artist_settings, artist_insights, connections
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .views import home, hall_of_fame, search, terms, partnerships, handler404, handler4042

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

    url(r'^sitepanel/', include(admin.site.urls)),
    url(r'^competitions/', include('competition.urls')),
    url(r'^artists/', include('artist.urls')),

    url(r'^connect/', include('socialconnector.urls')),
    url(r'^media/', include('media.urls')),
    url(r'^blog/', include('blog.urls')),

    #  userprofile
    url(r'^user/', include('userprofile.urls')),

    # api
    # url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('api_rest.urls')),

    # static pages
    url(r'^profile/$', login_required(single_artist), {"display": "profile"}, name="profile"),
    url(r'^profile/connections$', login_required(connections), {"display": "profile"}, name="connections"),
    url(r'^profile/insights/$', login_required(artist_insights), {"display":"profile"}, name="insights"),
    url(r'^settings/$', login_required(artist_settings), {"display":"profile"}, name="settings"),

    # static pages - phase 2
    url(r'^faq/$', 'content.views.faq', {}, name="faq"),
    url(r'^hall-of-fame/$', hall_of_fame, {}, name="hall_of_fame"),
    url(r'^search/$', search, {}, name="search"),
    url(r'^terms-and-conditions/$', terms, {}, name="terms"),
    url(r'^partnerships/$', partnerships, {}, name="partnerships"),
    url(r'^404/$', handler404, {}, name="handler404"),
    url(r'^404-2/$', handler4042, {}, name="handler404_2"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)