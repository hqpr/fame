from django import template
from django.conf import settings

from apps.media.models import AudioLike

register = template.Library()

@register.inclusion_tag('rating-large.html')
def audio(audio, user, display, size):
    if user:
        liked_audio = ""
        try:
            AudioLike.objects.get(fan=user, audio=audio)
            liked_audio = " active"
        except:
            pass
    # poll = Choice.objects.all()
    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'audio': audio,
        'display': display,
        'liked_audio': liked_audio,
        'size': size
    }
