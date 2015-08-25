import urllib
import datetime
import time
from base64 import decodestring
import re
import os

from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, UpdateView
import simplejson
from django.core import serializers
from social.apps.django_app.default.models import UserSocialAuth
import soundcloud
from django.conf import settings
import spotipy
import mixcloud

from .forms import AudioForm, AudioFileForm, PlayListForm, VideoFileForm, VideoForm
from apps.media.models import Audio, AudioPlaylist, Video, PlaylistItem, AudioComment
from apps.userprofile.models import Task1


class AudioFileView(FormView):
    template_name = 'add-audio-1.html'
    form_class = AudioFileForm

    def get_context_data(self, **kwargs):
        context = super(AudioFileView, self).get_context_data(**kwargs)

        # soundcloud
        try:
            token = UserSocialAuth.objects.get(user_id=self.request.user.id, provider='soundcloud')
            client = soundcloud.Client(use_ssl=False, access_token=token.access_token)
            context['soundcloud'] = client.get('/me/tracks')
        except:
            context['soundcloud'] = None

        # spotify
        try:
            sp = UserSocialAuth.objects.get(user_id=self.request.user.id, provider='spotify')
            token = sp.access_token
            sp_client = spotipy.Spotify(auth=token)
            try:
                results = sp_client.current_user_saved_tracks()
                tracks = []
                for item in results['items']:
                    tracks.append(item['track'])
                context['tracks'] = tracks
            except spotipy.SpotifyException:
                # Expired token
                sp.delete()
                context['tracks'] = None
        except UserSocialAuth.DoesNotExist:
            context['tracks'] = None

        # mixcloud
        try:
            token = UserSocialAuth.objects.get(user_id=self.request.user.id, provider='mixcloud')
            client = mixcloud.Mixcloud(access_token=token.access_token)
            mxcld = []
            for tracks in client.user(token.uid).cloudcasts():
                mxcld.append(tracks)
            context['mixcloud'] = mxcld
        except:
            context['mixcloud'] = None

        return context

    def form_valid(self, form):

        form.instance.user = self.request.user
        fs = form.save()
        data = {
            'success': True,
            'redirect_to': reverse('add_audio_step2', args=(fs.pk,)),
            'competition_add': reverse('competition_add_audio', args=(fs.pk,))
        }
        return HttpResponse(simplejson.dumps(data), content_type='application/json')


class AudioView(UpdateView):
    template_name = 'add-audio-2.html'
    form_class = AudioForm

    def get_context_data(self, **kwargs):
        context = super(AudioView, self).get_context_data(**kwargs)
        context.update({
            'form_action': reverse('add_audio_step2', args=(self.kwargs['object_id'],))
        })
        return context

    def get_object(self, queryset=None):
        obj = Audio.objects.get(id=self.kwargs['object_id'])
        return obj

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.is_complete = True
        form.save()
        data = {
            'success': True,
            'redirect_to': reverse('profile')
        }
        try:
            t = Task1.objects.get(user=self.request.user)
            t.task2 = True
            t.save()
        except Task1.DoesNotExist:
            Task1.objects.create(user=self.request.user, task2=True)

        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    def form_invalid(self, form):
        html = render_to_string(self.template_name, self.get_context_data(form=form))
        data = {
            'success': False,
            'html': html
        }
        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    def render_to_response(self, context, **response_kwargs):
        return super(AudioView, self).render_to_response(context, **response_kwargs)


class PlayListView(FormView):
    template_name = 'create-playlist.html'
    form_class = PlayListForm

    def get_context_data(self, **kwargs):
        context = super(PlayListView, self).get_context_data(**kwargs)
        context.update({
            'form_action': reverse('add_playlist')
        })
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        data = {
            'success': True,
            'redirect_to': reverse('profile')
        }
        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    def form_invalid(self, form):
        html = render_to_string(self.template_name, self.get_context_data(form=form))
        data = {
            'success': False,
            'html': html
        }
        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    def render_to_response(self, context, **response_kwargs):
        return super(PlayListView, self).render_to_response(context, **response_kwargs)

@csrf_exempt
def playlist_cover(request):
    f_name = 'img_%s_%d.jpg' % (request.user.id, int(datetime.datetime.now().strftime("%s")))
    if request.POST:
        f = open("server_media/playlists/%s/%s/%s/%s" % (time.strftime("%y"),
                                                         time.strftime("%m"),
                                                         time.strftime("%d"), f_name), "w+")
        _, b64data = request.POST['data'].split(',')
        f.write(decodestring(b64data))
        f.close()
        AudioPlaylist.objects.create(user=request.user, cover='playlists/%s/%s/%s/%s' % (time.strftime("%y"),
                                                                                         time.strftime("%m"),
                                                                                         time.strftime("%d"), f_name))
        return redirect('profile')
    pass

def trackcard(request, track_id):
    track = Audio.objects.get(id=track_id)
    track.plays += 1
    track.save()
    return render(request, 'trackcard.html', {'track': track})


class PlayListUpdateView(UpdateView):
    template_name = 'create-playlist.html'
    form_class = PlayListForm

    def get_context_data(self, **kwargs):
        context = super(PlayListUpdateView, self).get_context_data(**kwargs)
        context.update({
            'form_action': reverse('edit_playlist', args=(self.kwargs['object_id'],))
        })
        return context

    def get_object(self, queryset=None):
        obj = AudioPlaylist.objects.get(id=self.kwargs['object_id'])
        return obj

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        data = {
            'success': True,
            'redirect_to': reverse('profile')
        }
        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    def form_invalid(self, form):
        html = render_to_string(self.template_name, self.get_context_data(form=form))
        data = {
            'success': False,
            'html': html
        }
        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    def render_to_response(self, context, **response_kwargs):
        return super(PlayListUpdateView, self).render_to_response(context, **response_kwargs)


class AudioUpdateView(UpdateView):
    model = Audio
    template_name = 'edit-audio.html'
    form_class = AudioForm

    def get_context_data(self, **kwargs):
        context = super(AudioUpdateView, self).get_context_data(**kwargs)
        context['object_id'] = self.object.id
        return context

    def get_object(self, queryset=None):
        obj = Audio.objects.get(id=self.kwargs['object_id'])
        return obj

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        data = {
            'success': True,
            'redirect_to': reverse('profile')
        }
        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    def form_invalid(self, form):
        html = render_to_string(self.template_name, self.get_context_data(form=form))
        data = {
            'success': False,
            'html': html
        }
        return HttpResponse(simplejson.dumps(data), content_type='application/json')


class VideoFileView(FormView):

    def get_context_data(self, **kwargs):
        context = super(VideoFileView, self).get_context_data(**kwargs)
        try:
            context['youtube'] = UserSocialAuth.objects.get(user_id=self.request.user.id, provider='google-oauth2')
            context['vimeo'] = UserSocialAuth.objects.get(user_id=self.request.user.id, provider='google-oauth2')
        except UserSocialAuth.DoesNotExist:
            context['youtube'] = None
        return context

    template_name = 'add-video-1.html'
    form_class = VideoFileForm

    def form_valid(self, form):

        form.instance.user = self.request.user
        fs = form.save()
        data = {
            'success': True,
            'redirect_to': reverse('add_video_step2', args=(fs.pk,)),
            'competition_add_video': reverse('competition_add_video', args=(fs.pk,))
        }
        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    def form_invalid(self, form):
        data = {
            'success': False,
        }
        return HttpResponse(simplejson.dumps(data), content_type='application/json')


class VideoView(UpdateView):
    template_name = 'add-video-2.html'
    form_class = VideoForm

    def get_context_data(self, **kwargs):
        context = super(VideoView, self).get_context_data(**kwargs)
        context.update({
            'form_action': reverse('add_video_step2', args=(self.kwargs['object_id'],))
        })
        return context

    def get_object(self, queryset=None):
        obj = Video.objects.get(id=self.kwargs['object_id'])
        return obj

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.is_complete = True
        form.save()
        data = {
            'success': True,
            'redirect_to': reverse('profile')
        }
        try:
            t = Task1.objects.get(user=self.request.user)
            t.task2 = True
            t.save()
        except Task1.DoesNotExist:
            Task1.objects.create(user=self.request.user, task5=True)
        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    def form_invalid(self, form):
        html = render_to_string(self.template_name, self.get_context_data(form=form))
        data = {
            'success': False,
            'html': html
        }
        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    def render_to_response(self, context, **response_kwargs):
        return super(VideoView, self).render_to_response(context, **response_kwargs)


def videocard(request, video_id):
    video = Video.objects.get(id=video_id)
    video.plays += 1
    video.save()
    data = {'video': video}
    return render(request, 'videocard.html', data)

def playlistcard(request, playlist_id):
    playlist = AudioPlaylist.objects.get(id=playlist_id)
    audios = PlaylistItem.objects.filter(playlist_id=playlist_id)
    data = {'playlist': playlist,
            'audios': audios}
    return render(request, 'playlistcard.html', data)

def all_media(request):
    # audios = Audio.public_objects.all().order_by('-added')
    # videos = Video.objects.all().order_by('-added')
    # playlists = AudioPlaylist.objects.all().order_by('-added')
    template_data = {
        # "audios": audios,
        # "videos": videos,
        # "playlists": playlists
        "audios": True,
        "videos": True,
        "playlists": True
    }
    return render(request, 'media.html', template_data)

def all_tracks(request):
    # audios = Audio.public_objects.all().order_by('-added')
    template_data = {
        # "audios": audios
        "audios": True
    }
    return render(request, 'media.html', template_data)

def all_videos(request):
    # videos = Video.objects.all().order_by('-added')
    template_data = {
        # "videos": videos
        "videos": True
    }
    return render(request, 'media.html', template_data)

def all_playlists(request):
    # playlists = AudioPlaylist.objects.all().order_by('-added')
    template_data = {
        # "playlists": playlists
        "playlists": True
    }
    return render(request, 'media.html', template_data)

def add_to_playlist(request, track_id):
    lists = AudioPlaylist.objects.filter(user=request.user)
    audio = Audio.objects.get(id=track_id)
    data = {'lists': lists, 'audio': audio}
    if request.method == 'POST':
        playlist_id = request.POST.get('playlist_name', None)
        if playlist_id and track_id:
            try:
                exist = PlaylistItem.objects.order_by('-pk')[0]
                try:
                    PlaylistItem.objects.create(playlist_id=playlist_id, audio_id=track_id, ordering=exist.ordering+1)
                except IntegrityError:
                    data = {
                        'success': False,
                        'msg': 'Track is already in that list!'
                    }
                    return HttpResponse(simplejson.dumps(data), content_type='application/json')
            except IndexError:
                PlaylistItem.objects.create(playlist_id=playlist_id, audio_id=track_id, ordering=1)
                data = {
                    'success': True
                }
                return HttpResponse(simplejson.dumps(data), content_type='application/json')
        data = {
            'success': False
        }
        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    return render(request, 'add-to-playlist.html', data)

def publisher(request):
    if request.method == 'POST':

        action = request.POST.get('action', None)
        if action == 'dzsap_front_submitcomment':
            playerid = request.POST.get('playerid', None)
            data = request.POST.get('postdata', None)
            times = re.findall('style=\"left\:(.*)\%\"', data)
            AudioComment.objects.create(audio_id=playerid, fan=request.user, comment=data,
                                        time=times[0])
        elif action == 'dzsap_get_comments':
            playerid = request.POST.get('playerid', None)
            try:
                comments = AudioComment.objects.filter(audio_id=playerid, approved=True)
                d = serializers.serialize('json', comments)
                return HttpResponse(d, content_type='application/json')
            except AudioComment.DoesNotExist:
                pass

        return HttpResponse('')


def soundcloud_import(request):
    if request.method == 'POST':
        sound_file = request.POST.get('download', None)
        track_id = request.POST.get('track_id', None)
        if sound_file and track_id:
            token = UserSocialAuth.objects.get(user=request.user, provider='soundcloud')
            client = soundcloud.Client(use_ssl=False, access_token=token.access_token)
            track_info = client.get('/tracks/%s' % track_id)

            download_url = '%s?client_id=%s' % (sound_file, settings.SOCIAL_AUTH_SOUNDCLOUD_KEY)
            audiopath = 'audios/%s/%s/%s/' % (time.strftime("%y"), time.strftime("%m"), time.strftime("%d"))
            fullfilename = os.path.join('%s/%s', '%s.mp3') % (settings.MEDIA_ROOT, audiopath, track_id)
            try:
                urllib.urlretrieve(download_url, fullfilename)
            except IOError:
                os.makedirs(os.path.join('%s/%s') % (settings.MEDIA_ROOT, audiopath))
            urllib.urlretrieve(download_url, fullfilename)

            a_name = '%s%s.mp3' % (audiopath, track_id)

            artwork_url = track_info.obj['artwork_url']
            coverpath = 'audios/covers/%s/%s/%s/' % (time.strftime("%y"), time.strftime("%m"), time.strftime("%d"))
            coverfilename = os.path.join('%s/%s', '%s.jpg') % (settings.MEDIA_ROOT, coverpath, track_id)

            # ToDo: save picture properly. Some handshake error on urlopen
            try:
                resource = urllib.urlopen(artwork_url)
                output = open(coverfilename, 'wb')
                output.write(resource.read())
                output.close()
                c_name = '%s%s.jpg' % (coverpath, track_id)
            except:
                c_name = artwork_url

            try:
                Audio.objects.get(user=request.user, soundcloud_track_id=track_id)
                data = {'success': False, 'msg': 'You\'re already imported that track into Fame'}
            except Audio.DoesNotExist:
                Audio.objects.create(name=track_info.obj['title'], user=request.user,
                                     artist=track_info.user['username'], audio=a_name,
                                     is_complete=True, soundcloud_track_id=track_id, cover=c_name)
                data = {'success': True}
        else:
            data = {'success': False, 'msg': 'Please, choose a track.'}
    else:
        data = {'success': False}
    return HttpResponse(simplejson.dumps(data), content_type='application/json')


def share(request, uid):
    try:
        obj = Audio.objects.get(uid=uid)
    except Audio.DoesNotExist:
        obj = Video.objects.get(uid=uid)
    except Video.DoesNotExist:
        obj = None
    return render(request, 'share.html', {'obj': obj})
