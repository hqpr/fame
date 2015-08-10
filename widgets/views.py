from django.shortcuts import render
from media.models import Audio


def trackcard(request, uid):
    try:
        track = Audio.objects.get(uid=uid, privacy='public')
    except Audio.DoesNotExist:
        track = None
    data = {
        'track': track
    }
    return render(request, 'widget-trackcard.html', data)
