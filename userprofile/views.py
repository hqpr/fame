from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.contrib.auth import authenticate, login
import simplejson
from django.contrib.auth import logout
from django.views.generic import FormView
from .forms import UserForm, UserProfile


def login_view(request):
    """View all login"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                data = {
                    'success': True,
                    'msg': 'User is valid, active and authenticated'
                }
                return HttpResponse(simplejson.dumps(data), content_type='application/json')
            else:
                data = {
                    'success': False,
                    'msg': 'The password is valid, but the account has been disabled!'
                }
                return HttpResponse(simplejson.dumps(data), content_type='application/json')
        else:
            data = {
                'success': False,
                'msg': 'The username and password were incorrect.'
            }
            return HttpResponse(simplejson.dumps(data), content_type='application/json')

    template_name = 'login.html'
    template_data = {
        "string": "Login Page",
    }
    return render(request, template_name, template_data)


class RegistrationView(FormView):
    template_name = 'register_step_1.html'
    form_class = UserForm

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        # context.update({
        #     'form_action': reverse('register_step_2', args=(self.kwargs['object_id'],))
        # })
        return context

    def form_valid(self, form):
        # form.instance.user = self.request.user
        # form.instance.is_complete = True
        # form.save()
        data = {
            'success': True,
            'redirect_to': reverse('profile')
        }
        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    def form_invalid(self, form):
        data = {
            'success': False,
        }
        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    def render_to_response(self, context, **response_kwargs):
        return super(RegistrationView, self).render_to_response(context, **response_kwargs)

def check_username(request):
    """ check if username is available """
    success = False
    if request.POST:
        username = request.POST.get('username', '')
        if len(username) >= 3:
            try:
                User.objects.get(username=username)
                success = False
            except User.DoesNotExist:
                success = True
    return HttpResponse(simplejson.dumps({'success': success}), content_type='application/json')


def logout_view(request):
    logout(request)
    return redirect('all_competitions')