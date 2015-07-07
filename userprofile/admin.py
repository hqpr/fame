from django.contrib import admin
from .models import UserProfile, HallOfFame, HallOfFameArtists

from suit.admin import SortableTabularInline

class HallOfFameArtistsInline(SortableTabularInline):
    model = HallOfFameArtists
    sortable = 'ordering'

class HallOfFameAdmin(admin.ModelAdmin):
    """Handle Hall Of Fame"""
    model = HallOfFame
    inlines = [HallOfFameArtistsInline]

admin.site.register(UserProfile)
admin.site.register(HallOfFame, HallOfFameAdmin)