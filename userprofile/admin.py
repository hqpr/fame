from django.contrib import admin
from .models import UserProfile, HallOfFame, HallOfFameArtists, UserSocial

from suit.admin import SortableTabularInline

class HallOfFameArtistsInline(SortableTabularInline):
    model = HallOfFameArtists
    sortable = 'ordering'

class HallOfFameAdmin(admin.ModelAdmin):
    """Handle Hall Of Fame"""
    model = HallOfFame
    inlines = [HallOfFameArtistsInline]

# class UserSocialAdmin(admin.ModelAdmin):
#     model = UserSocial

admin.site.register(UserProfile)
admin.site.register(UserSocial)
admin.site.register(HallOfFame, HallOfFameAdmin)