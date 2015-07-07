from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from social.apps.django_app.default.models import UserSocialAuth
from media.models import Audio, Video, AudioPlaylist, PlaylistItem
from instagram.client import InstagramAPI
from django.conf import settings

from .models import UserRoles
from userprofile.models import UserProfile


# Create your views here.
def artists(request):
    """View all artists"""

    template_name = 'artists.html'
    artists = UserProfile.objects.filter(user__in=[i.user for i in UserRoles.objects.filter(roles=1,user__in=User.objects.all())])
    print User.objects.all()
    print artists

    template_data = {
        "string": "All Artists Page",
        "artists": artists
    }

    return render_to_response(template_name,
                              template_data,
                              context_instance=RequestContext(request)
    )

def single_artist(request, *args, **kwargs):
    """View single artist"""
    if "slug" in kwargs:
        try:
            username = kwargs["slug"]
            user = User.objects.get(username=username)
            display = "artist"
        except:
            return HttpResponse("Error")
    else:
        if not request.user.is_authenticated:
            return HttpResponse("Error")
        user = request.user
        display = "profile"

    string = get_profile_string(kwargs, user)
    audios = Audio.objects.filter(user=user, is_complete=True).order_by('-added')
    playlists = AudioPlaylist.objects.filter(user=user)[:4]
    videos = Video.objects.filter(user=user, is_complete=True).order_by('-added')[:2]

    try:
        a = UserSocialAuth.objects.get(user_id=user.id, provider='instagram')
        access_token = a.access_token
        api = InstagramAPI(access_token=access_token, client_secret=settings.SOCIAL_AUTH_INSTAGRAM_SECRET)
        recent_media, next_ = api.user_recent_media(user_id=int(a.uid), count=23)
        imgs = []
        for media in recent_media:
            imgs.append(media.images['standard_resolution'].url)
        instagram = imgs
        nickname = str(api.user()).split(':')[1].replace(' ', '')
    except UserSocialAuth.DoesNotExist:
        instagram = ''
        nickname = ''

    template_name = 'single-artist.html'
    template_data = {
        "string": string,
        'audios': audios,
        'instagram': instagram,
        'nickname': nickname,
        'playlists': playlists,
        'videos': videos,
        'user': user,
        'display': display
    }

    return render_to_response(template_name,
                              template_data,
                              context_instance=RequestContext(request)
    )

def artist_settings(request, *args, **kwargs):
    """View settings page"""

    template_name = 'settings.html'
    template_data = {
        "string": "Settings Page",
    }

    return render_to_response(template_name,
                              template_data,
                              context_instance=RequestContext(request)
    )


def artist_insights(request, *args, **kwargs):
    """View insights page"""

    template_name = 'insights.html'
    template_data = {
        "string": "Insights Page",
    }

    return render_to_response(template_name,
                              template_data,
                              context_instance=RequestContext(request)
    )


'''Handle complicated views'''

def get_profile_string(kwargs, user):
    if "display" in kwargs:
        display = kwargs["display"]

        string = "Single artist profile"

        if display == "profile":
            string = "My artist profile"
        elif display in ['type','type_id']:
            item_type = "Track"
            if "type" in kwargs:
                type_to_check = kwargs["type"]

                if type_to_check == "m":
                    item_type = "Music"
                elif type_to_check == "p":
                    item_type = "Playlist"
                elif type_to_check == "v":
                    item_type = "Video"

            string = "Track type: %s" % (item_type,)

            if "type_id" in kwargs:
                type_id = kwargs["type_id"]
                string += " - ID %s" % (type_id,)

    return string

def connections(request, *args, **kwargs):
    """Return all connections following"""
    return render(request, "connections.html",{})