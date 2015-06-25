from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from social.apps.django_app.default.models import UserSocialAuth
import soundcloud
from .models import UserPhoto, UserAudio, UserVideo, VideoPlaylist
from django.views.generic import FormView
# from .forms import AudioForm, PhotoForm, VideoForm
import gdata.youtube
import gdata.youtube.service

from datetime import timedelta
import httplib2
import sys

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets, OAuth2WebServerFlow
from oauth2client.tools import run
from optparse import OptionParser
from instagram.client import InstagramAPI
import mixcloud

from base64 import decodestring
from datetime import date
import datetime

DROPBOX_PROVIDER = 'dropbox-oauth2'
SOUNDCLOUD_PROVIDER = 'soundcloud'
GOOGLE_PROVIDER = 'google-oauth2'


@login_required()
def home(request):
    access_token = request.GET.get('access_token')
    data = {'access_token': access_token}
    return render(request, 'index.html', data)


@csrf_exempt
def back(request, backend, *args, **kwargs):

    access_token = request.GET.get('extra_data')
    try:
        backend_response = UserSocialAuth.objects.get(user_id=request.user.id, provider=backend)

    except UserSocialAuth.DoesNotExist:
        backend_response = None

    if backend == DROPBOX_PROVIDER:
        drbx_lnk = True
    else:
        drbx_lnk = False

    data = {
        'access_token': access_token,
        'backend_response': backend_response,
        'backend': backend,
        'drbx_lnk': drbx_lnk
    }
    return render(request, 'backend.html', data)


def drop_ls(request):
    import dropbox
    backend_response = UserSocialAuth.objects.get(user_id=request.user.id, provider=DROPBOX_PROVIDER)
    code = str(backend_response.access_token)
    client = dropbox.client.DropboxClient(code)

    print 'linked account: ', client.account_info()

    folder_metadata = client.metadata('/')

    data = {
        'folder_metadata': folder_metadata
    }
    return render(request, 'drop.html', data)


# class PhotoView(FormView):
#     template_name = 'image_upload.html'
#     form_class = PhotoForm
#
#     def get_context_data(self, **kwargs):
#         context = super(PhotoView, self).get_context_data(**kwargs)
#         context['photos'] = UserPhoto.objects.filter(user=self.request.user)
#         return context
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         form.save()
#         return redirect('upload_photo')


# SoundCloud
# https://developers.soundcloud.com/docs/api/guide#uploading-files
# class AudioView(FormView):
#     template_name = 'sound_upload.html'
#     form_class = AudioForm
#
#     def get_context_data(self, **kwargs):
#         context = super(AudioView, self).get_context_data(**kwargs)
#         # context['audios'] = UserAudio.objects.filter(user=self.request.user)
#         # token = UserSocialAuth.objects.get(user_id=self.request.user.id, provider='soundcloud')
#         # try:
#             # client = soundcloud.Client(access_token=token.access_token)
#             # context['current_user'] = client.get('/me/tracks')
#             # context['suser'] = token.uid
#         # except:
#         #     context['current_user'] = None
#         return context
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         form.save()
#         return redirect('upload_sound')


# class VideoView(FormView):
#     template_name = 'video_upload.html'
#     form_class = VideoForm
#
#     def get_context_data(self, **kwargs):
#         context = super(VideoView, self).get_context_data(**kwargs)
#         context['videos'] = UserVideo.objects.filter(user=self.request.user)
#         context['playlist'] = VideoPlaylist.objects.filter(user=self.request.user)
#
#         return context
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         form.save()
#         return redirect('upload_video')


def create_playlist(request):
    if request.POST:
        try:
            playlist_name = request.POST['title']
            print playlist_name
            VideoPlaylist.objects.create(title=playlist_name, user=request.user)
            return redirect('upload_video')
        except:
            return HttpResponse('error')
    return render(request, 'create_playlist.html')


def add_to_playlist(request):
    if 'video_id' in request.GET:
        video_id = request.GET.get('video_id', None)
        playlist_id = request.GET.get('playlist_id', None)
        pl = get_object_or_404(VideoPlaylist, id=playlist_id)
        v = get_object_or_404(UserVideo, id=video_id)
        pl.videos.add(v)
        return redirect('upload_video')


# http://stackoverflow.com/questions/16396433/django-oauth2-google-not-working-on-server
def youtube_view(request):
    yt_service = gdata.youtube.service.YouTubeService()
    yt_service.ssl = True

    YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.readonly",
                      "https://www.googleapis.com/auth/yt-analytics.readonly"]
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    YOUTUBE_ANALYTICS_API_SERVICE_NAME = "youtubeAnalytics"
    YOUTUBE_ANALYTICS_API_VERSION = "v1"
    CLIENT_SECRETS_FILE = 'client_secrets.json'

    now = datetime.now()
    one_day_ago = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    one_week_ago = (now - timedelta(days=7)).strftime("%Y-%m-%d")

    parser = OptionParser()
    parser.add_option("--metrics", dest="metrics", help="Report metrics",
                      default="views,comments,favoritesAdded,favoritesRemoved,likes,dislikes,shares")
    parser.add_option("--dimensions", dest="dimensions", help="Report dimensions",
                      default="video")
    parser.add_option("--start-date", dest="start_date",
                      help="Start date, in YYYY-MM-DD format", default=one_week_ago)
    parser.add_option("--end-date", dest="end_date",
                      help="End date, in YYYY-MM-DD format", default=one_day_ago)
    parser.add_option("--start-index", dest="start_index", help="Start index",
                      default=1, type="int")
    parser.add_option("--max-results", dest="max_results", help="Max results",
                      default=10, type="int")
    parser.add_option("--sort", dest="sort", help="Sort order", default="-views")
    (options, args) = parser.parse_args()

    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=" ".join(YOUTUBE_SCOPES))

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()
    credentials = run(flow, storage)

    http = credentials.authorize(httplib2.Http())
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=http)
    youtube_analytics = build(YOUTUBE_ANALYTICS_API_SERVICE_NAME,
                              YOUTUBE_ANALYTICS_API_VERSION, http=http)

    channels_response = youtube.channels().list(
        mine=True,
        part="id"
    ).execute()
    greetings = []
    v = []
    for channel in channels_response.get("items", []):
        channel_id = channel["id"]

        analytics_response = youtube_analytics.reports().query(
            ids="channel==%s" % channel_id,
            metrics=options.metrics,
            dimensions=options.dimensions,
            start_date=options.start_date,
            end_date=options.end_date,
            start_index=options.start_index,
            max_results=options.max_results,
            sort=options.sort
        ).execute()

        print "Analytics Data for Channel %s" % channel_id

        greetings.append("Analytics Data for Channel %s" % channel_id)

        for column_header in analytics_response.get("columnHeaders", []):
            print "%-20s" % column_header["name"],

        for row in analytics_response.get("rows", []):
            for value in row:
                print "%-20s" % value
                v.append("%-20s" % value)
    data = {'greetings': greetings, 'analytics_response': channels_response.get("items", [])}

    return render(request, 'yt_console.html', data)


@csrf_exempt
def imageupload(request):
    f_name = 'img_%s_%d.jpg' % (request.user.id, int(datetime.datetime.now().strftime("%s")))
    if request.POST:
        f = open("server_media/images/uploads/%s" % f_name, "w")
        _, b64data = request.POST['data'].split(',')
        f.write(decodestring(b64data))
        f.close()
        UserPhoto.objects.create(user=request.user, image='server_media/images/uploads//%s' % f_name)
        return redirect('profile')
    pass

# https://github.com/vimeo/vimeo.py

def insta(request):
    try:
        a = UserSocialAuth.objects.get(user_id=request.user.id, provider='instagram')
        access_token = a.access_token
        api = InstagramAPI(access_token=access_token, client_secret=settings.SOCIAL_AUTH_INSTAGRAM_SECRET)
        recent_media, next_ = api.user_recent_media(user_id=int(a.uid), count=10)
        imgs = []
        for media in recent_media:
            imgs.append(media.images['standard_resolution'].url)
        data = {'instagram': imgs}
        return render(request, 'insta.html', data)
    except UserSocialAuth.DoesNotExist:
        return render(request, 'insta.html', {})


# https://github.com/emillon/mixcloud
def mixcl(request):
    try:
        lst = []
        a = UserSocialAuth.objects.get(user_id=request.user.id, provider='mixcloud')
        m = mixcloud.Mixcloud(access_token=a.access_token)
        u = m.user(a.uid)
        for c in u.cloudcasts():
            lst.append(c.name)
        data = {'mixcloud': lst, 'm': m}
        return render(request, 'mixcloud.html', data)
    except UserSocialAuth.DoesNotExist:
        return render(request, 'mixcloud.html', {})