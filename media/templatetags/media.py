from django import template
from media.models import Audio, AudioLike
register = template.Library()

@register.inclusion_tag('rating-large.html', takes_context=True)
def audio_rating(audio_id, size, user):
    if user:
        liked_audio = ""
        try:
            liked_audio = " active"
        except:
            pass
    # poll = Choice.objects.all()
    return { 'liked_audio' : liked_audio }