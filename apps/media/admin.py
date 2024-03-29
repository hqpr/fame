from django.contrib import admin
from suit.admin import SortableTabularInline
from modeltranslation.admin import TranslationAdmin

from apps.media.models import Audio, Genre, Image, Video, AudioPlaylist, PlaylistItem, AudioComment

# Register your models here.
class GenreAdmin(admin.ModelAdmin):
    """Handle Genre"""
    model = Genre

class AudioAdmin(TranslationAdmin):
    """Handle Audio"""
    model = Audio

class ImageAdmin(admin.ModelAdmin):
    """Handle Image"""
    model = Image

class VideoAdmin(admin.ModelAdmin):
    """Handle Video"""
    model = Video

class PlaylistItemInline(SortableTabularInline):
    model = PlaylistItem
    sortable = "ordering"

class AudioPlaylistAdmin(admin.ModelAdmin):
    """Handle Audio"""
    model = AudioPlaylist
    inlines = [PlaylistItemInline]


class AudioCommentAdmin(admin.ModelAdmin):
    model = AudioComment

admin.site.register(Genre, GenreAdmin)
admin.site.register(Audio, AudioAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(AudioPlaylist, AudioPlaylistAdmin)
admin.site.register(AudioComment, AudioCommentAdmin)
