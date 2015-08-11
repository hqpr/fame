from modeltranslation.translator import translator, TranslationOptions

from apps.media.models import Audio


class AudioTranslationOptions(TranslationOptions):
    fields = ('name', 'artist', 'genre', 'description')

translator.register(Audio, AudioTranslationOptions)
