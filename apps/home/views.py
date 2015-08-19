from django.http import HttpResponse
from django.shortcuts import render
import simplejson
from .models import Tutorial

def home(request):
    return render(request, 'homepage.html', {})

def complete_tutorial(request):
    if request.method == 'POST':
        Tutorial.objects.create(user=request.user, is_complete=True)
        return HttpResponse(simplejson.dumps({'success': True}), content_type='application/json')


