from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, UpdateView
import simplejson
from .forms import AudioForm, AudioFileForm, PlayListForm
from .models import Audio, VideoPlaylist
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
    template_name = 'create_playlist.html'
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
        VideoPlaylist.objects.create(user=request.user, cover='playlists/%s/%s/%s/%s' % (time.strftime("%y"),
                                                                                         time.strftime("%m"),
                                                                                         time.strftime("%d"), f_name))
        return redirect('profile')
    pass


def trackcard(request, track_id):
    track = Audio.objects.get(id=track_id)
    return render(request, 'trackcard.html', {'track': track})


class AudioUpdateView(UpdateView):
    model = Audio
    template_name = 'edit_audio.html'
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
