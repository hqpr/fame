from django.conf import settings
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from artist.views import single_artist, artist_settings, artist_insights
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

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
    url(r'^$', 'fame.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),

    url(r'^sitepanel/', include(admin.site.urls)),
    url(r'^competitions/', include('competition.urls')),
    url(r'^artists/', include('artist.urls')),

    url(r'^connect/', include('socialconnector.urls')),
    url(r'^media/', include('media.urls')),

    #  userprofile
    url(r'^user/', include('userprofile.urls')),

    # api
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/test/', include(router.urls)),

    # static pages
    url(r'^profile/$', login_required(single_artist), {"display":"profile"}, name="profile"),
    url(r'^profile/insights/$', artist_insights, {"display":"profile"}, name="insights"),
    url(r'^settings/$', artist_settings, {"display":"profile"}, name="settings"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)