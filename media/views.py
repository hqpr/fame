from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, UpdateView
import simplejson
from .forms import AudioForm, AudioFileForm, PlayListForm, VideoFileForm, VideoForm
from .models import Audio, AudioPlaylist, Video, PlaylistItem
import datetime
import time
from base64 import decodestring


class AudioFileView(FormView):
    template_name = 'add-audio-1.html'
    form_class = AudioFileForm

    def form_valid(self, form):

        form.instance.user = self.request.user
        fs = form.save()
        data = {
            'success': True,
            'redirect_to': reverse('add_audio_step2', args=(fs.pk,))
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
    return render(request, 'trackcard.html', {'track': track})


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
    template_name = 'add-video-1.html'
    form_class = VideoFileForm

    def form_valid(self, form):

        form.instance.user = self.request.user
        fs = form.save()
        data = {
            'success': True,
            'redirect_to': reverse('add_video_step2', args=(fs.pk,))
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
    data = {'video': video}
    return render(request, 'videocard.html', data)

def all_media(request):
    return render(request, 'hall-of-fame.html', {})

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
