from django.contrib import admin
from .models import UserProfile, UserGenre, HallOfFame, HallOfFameArtists, UserSocial

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

class UserGenreInline(admin.TabularInline):
    model = UserGenre

class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    inlines = [UserGenreInline]


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserSocial)
admin.site.register(HallOfFame, HallOfFameAdmin)