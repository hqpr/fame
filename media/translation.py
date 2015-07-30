from modeltranslation.translator import translator, TranslationOptions
from .models import Audio

class AudioTranslationOptions(TranslationOptions):
    fields = ('name', 'artist', 'genre', 'description')

translator.register(Audio, AudioTranslationOptions)
