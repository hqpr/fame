from sets import Set
from datetime import timedelta

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from social.apps.django_app.default.models import UserSocialAuth
from instagram.client import InstagramAPI
from django.conf import settings

from apps.media.models import Audio, Video, AudioPlaylist
from .models import UserRoles, UserConnections
from .forms import UserProfileForm, UserForm
from apps.userprofile.models import UserProfile, UserSocial, UserStatus
from apps.subscription.models import Subscription


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
    social = UserSocial.objects.filter(user=UserProfile.objects.get(user=user))
    if len(social):
        social = {i.account:i.link for i in social}
    user_status = ""
    genres = None
    if audios:
        genres = Set([i.genre for i in audios])

    user_status_list = UserStatus.objects.filter(user=UserProfile.objects.get(user=user)).order_by('-created')
    if len(user_status_list):
        user_status = user_status_list[0].status

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
        'display': display,
        'social': social,
        'user_status': user_status,
        'genres': genres
    }

    return render_to_response(template_name,
                              template_data,
                              context_instance=RequestContext(request)
    )

@login_required
def artist_settings(request, *args, **kwargs):
    """View settings page"""
    user_form = UserForm(instance=request.user,prefix="usf")
    userprofile = UserProfile.objects.get(user=request.user)
    user_profile_form = UserProfileForm(prefix="usp", instance=UserProfile.objects.get(user=request.user))
    social = UserSocial.objects.filter(user=UserProfile.objects.get(user=request.user))
    if len(social):
        social = {i.account:i.link for i in social}
    user_status = ""

    try:
        UserProfile.objects.get(user=request.user, is_pro=True)
        end_date = Subscription.objects.get(user=request.user).end_date
    except Subscription.MultipleObjectsReturned:
        end_date = Subscription.objects.filter(user=request.user)\
                          .latest('charge_date').end_date
    except (Subscription.DoesNotExist, UserProfile.DoesNotExist):
        end_date = None

    if request.POST:
        user_form = UserForm(request.POST,prefix="usf", instance=request.user)
        user_profile_form = UserProfileForm(request.POST, prefix="usp", instance=UserProfile.objects.get(user=request.user))
        # Ensure both forms are valid before continuing on
        if user_form.is_valid() and user_profile_form.is_valid():
            user_profile_form.save()
            user_form.save()
            if "password" in request.POST and len(request.POST["password"]) > 5:
                u = request.user
                u.set_password(request.POST["password"])
                u.save()
            return HttpResponseRedirect(reverse("settings"))
    template_name = 'settings.html'
    template_data = {
        "profile": "User Profile",
        "user_form": user_form,
        "user_profile_form": user_profile_form,
        'end_date': end_date,
        'social': social,
        'user_status': user_status
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

@login_required
def connections(request, *args, **kwargs):
    """Return all connections following"""
    user_connections = UserConnections.objects.filter(user=request.user)
    template_data = {
        "total_connections": user_connections
    }
    return render(request, "connections.html",template_data)