from django.shortcuts import render, render_to_response
from django.template import RequestContext

from userprofile.models import HallOfFameArtists, UserProfile
from competition.models import Competition
from media.models import Audio

def home(request):
    return render(request, 'home.html', {})

def hall_of_fame(request):
    args = {
        "hall_of_fame__id": 1
    }
    try:
        args["type"] = request.GET["type"]
    except:
        pass

    hall_of_famers = HallOfFameArtists.objects.filter(**args).order_by('ordering')
    
    template_data = {
        "hall_of_famers": hall_of_famers
    }

    return render(request, 'hall-of-fame.html', template_data)

def search(request):
    artists = None
    competitions = None
    tracks = None
    results = None

    if "q" in request.GET and len(request.GET["q"]):
        query = request.GET["q"]
        try:
            artists = UserProfile.objects.filter(display_name__icontains=query)[:10]
        except:
            pass
        try:
            competitions = Competition.published_objects.filter(name__icontains=query)[:10]
        except:
            pass

        try:
            tracks = Audio.public_objects.filter(name__icontains=query)[:10]
        except:
            pass
        if len(artists) or len(competitions) or len(tracks):
            results = True

    template_data = {
        "results": results,
        "artists": artists,
        "competitions": competitions,
        "tracks": tracks

    }
    return render(request, 'search.html', template_data)

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