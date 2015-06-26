from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import FormView
import simplejson
from .forms import AudioForm, AudioFileForm, PlayListForm


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

class AudioView(FormView):
    template_name = 'add-audio-2.html'
    form_class = AudioForm

    def get_context_data(self, **kwargs):
        context = super(AudioView, self).get_context_data(**kwargs)
        context.update({
            'form_action': reverse('add_audio_step2', args=(self.kwargs['object_id'],))
        })
        return context

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