from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
import simplejson
from django.contrib.auth import logout
from django.views.generic import FormView
from .forms import UserForm, UserProfileForm
from .models import UserProfile
from django.core.exceptions import PermissionDenied


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
    """ for drag-n-drop. Not using yet """
    if request.POST:
        picture = request.POST.get('id_picture', None)
        if picture:
            u = UserProfile.objects.get(user_id=object_id)
            u.picture = picture
            u.save()

def complete_registration(request):
    user = UserProfile.objects.get(user=request.user)
    data = {'user': user}
    return render(request, 'register_complete.html', data)

def logout_view(request):
    logout(request)
    return redirect('home')
