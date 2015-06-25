from django.contrib import admin

from .models import Audio, Genre, Image, Video

# Register your models here.
class GenreAdmin(admin.ModelAdmin):
    """Handle Genre"""
    model = Genre

class AudioAdmin(admin.ModelAdmin):
    """Handle Audio"""
    model = Audio

class ImageAdmin(admin.ModelAdmin):
    """Handle Image"""
    model = Image

class VideoAdmin(admin.ModelAdmin):
    """Handle Video"""
    model = Video

admin.site.register(Genre, GenreAdmin)
admin.site.register(Audio, AudioAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Video, VideoAdmin)