from django.http import HttpResponse
from django.shortcuts import render
import simplejson
from .models import Tutorial
from apps.userprofile.models import Task1
from social.apps.django_app.default.models import UserSocialAuth

from apps.blog.models import BlogItem
from apps.resources.models import ResourcesItem

def home(request):
    if request.user.is_authenticated():
        try:
            task1 = Task1.objects.get(user=request.user)
        except Task1.DoesNotExist:
            task1 = None
        try:
            social = UserSocialAuth.objects.filter(user=request.user).count()
            if social > 2:
                try:
                    s = Task1.objects.get(user=request.user)
                    s.task3 = True
                    s.save()
                except Task1.DoesNotExist:
                    Task1.objects.create(user=request.user, task3=True)
        except UserSocialAuth.DoesNotExist:
            pass
        
        news = BlogItem.published_objects.order_by('-publish_date')[:4]
        resources = ResourcesItem.published_objects.order_by('-publish_date')[:4]

        template_data = {
            "news": news,
            "resources": resources,
            'task1': task1
        }
        return render(request, 'homepage.html', template_data)
    return render(request, 'home.html', {})


def complete_tutorial(request):
    if request.method == 'POST':
        Tutorial.objects.create(user=request.user, is_complete=True)
        return HttpResponse(simplejson.dumps({'success': True}), content_type='application/json')


