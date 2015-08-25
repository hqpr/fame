from django.contrib import admin
from suit.admin import SortableTabularInline

from apps.userprofile.models import UserProfile, UserGenre, HallOfFame, HallOfFameArtists, UserSocial, \
    Badges, Task1


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

class BadgesAdmin(admin.ModelAdmin):
    model = Badges

class Task1Admin(admin.ModelAdmin):
    model = Task1

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserSocial)
admin.site.register(HallOfFame, HallOfFameAdmin)
admin.site.register(Badges, BadgesAdmin)
admin.site.register(Task1, Task1Admin)
