from base64 import decodestring
import datetime
import time

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
import simplejson
from django.contrib.auth import logout
from django.views.generic import FormView
from django.core.exceptions import PermissionDenied

from apps.userprofile.forms import UserForm, UserProfileForm, UserSocialForm
from .models import UserProfile, UserSocial


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

    def form_valid(self, form):
        form.instance.user = self.request.user

        fs = form.save()
        data = {
            'success': True,
            'redirect_to': reverse('register_step_2', args=(fs.pk,))
        }
        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    def form_invalid(self, form):
        data = {
            'success': False,
        }
        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    def save(self, commit=True):
        user = super(RegistrationView, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def render_to_response(self, context, **response_kwargs):
        return super(RegistrationView, self).render_to_response(context, **response_kwargs)


class RegistrationStepView(FormView):
    """ Second step """
    template_name = 'register_step_2.html'
    form_class = UserProfileForm

    def get_context_data(self, **kwargs):
        context = super(RegistrationStepView, self).get_context_data(**kwargs)
        context.update({
            'form_action': reverse('register_step_2', args=(self.kwargs['object_id'],))
        })
        context['object_id'] = self.kwargs['object_id']
        return context

    def form_valid(self, form, **kwargs):
        user = User.objects.get(id=self.kwargs['object_id'])
        try:
            UserProfile.objects.get(user_id=self.kwargs['object_id'])
            raise PermissionDenied
        except UserProfile.DoesNotExist:
            form.instance.user = user
            form.instance.is_complete = True
            form.save()

            # log user in
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(self.request, user)
            data = {
                'success': True,
                'redirect_to': reverse('complete_registration')
            }
            return HttpResponse(simplejson.dumps(data), content_type='application/json')

    def form_invalid(self, form):
        print form
        html = render_to_string(self.template_name, self.get_context_data(form=form))
        data = {
            'success': False,
            'html': html
        }
        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    def render_to_response(self, context, **response_kwargs):
        return super(RegistrationStepView, self).render_to_response(context, **response_kwargs)

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

def upload_avatar(request, object_id):
    """ for drag-n-drop """
    if request.POST:
        f_name = 'img_%s_%d.jpg' % (request.user.id, int(datetime.datetime.now().strftime("%s")))
        f = open("server_media/avatars/%s/%s/%s/%s" % (time.strftime("%y"),
                                                       time.strftime("%m"),
                                                       time.strftime("%d"),
                                                       f_name), "w")
        _, b64data = request.POST['data'].split(',')
        f.write(decodestring(b64data))
        f.close()
        u = UserProfile.objects.get(user_id=object_id)
        u.picture = 'avatars/%s/%s/%s/%s' % (time.strftime("%y"),
                                           time.strftime("%m"),
                                           time.strftime("%d"),
                                           f_name)
        u.save()
    return HttpResponse(simplejson.dumps({'success': True}), content_type='application/json')

def complete_registration(request):
    user = UserProfile.objects.get(user=request.user)
    data = {'user': user}
    return render(request, 'register_complete.html', data)

def logout_view(request):
    logout(request)
    return redirect('home')


def user_home(request):
    return render(request, 'homepage.html', {})


class SocialView(FormView):
    template_name = 'edit-social.html'
    form_class = UserSocialForm

    def form_valid(self, form):

        form.instance.user = UserProfile.objects.get(user=self.request.user)
        # fs = form.save()
        try:
            user_social_object = UserSocial.objects.get(account=form.instance.account,user=form.instance.user)
            user_social_object.link = form.instance.link
            user_social_object.save()
        except:
            user_social_object = UserSocial(**{'user':form.instance.user,'account':form.instance.account,'link':form.instance.link})
            user_social_object.save()

        data = {
            'success': True,
        }
        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    def form_invalid(self, form):
        data = {
            'success': False,
        }
        return HttpResponse(simplejson.dumps(data), content_type='application/json')