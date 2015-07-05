from django.shortcuts import render, render_to_response
from django.template import RequestContext

def home(request):
    return render(request, 'home.html', {})

def hall_of_fame(request):
    return render(request, 'hall-of-fame.html', {})

def search(request):
    return render(request, 'search.html', {})

def terms(request):
    return render(request, 'terms.html', {})

def partnerships(request):
    return render(request, 'partnerships.html', {})

def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

def handler4042(request):
    response = render_to_response('404-2.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response