from apps.userprofile.models import UserProfile, UserBadges
from apps.artist.views import UserConnections
from apps.home.models import Tutorial

def check_profile(request):
    if request.user.is_authenticated():
        try:
            UserProfile.objects.get(user=request.user)
            return {'valid': 1}
        except UserProfile.DoesNotExist:
            return {'valid': 0, 'user_id': request.user.id}
    return {'valid': 1}

def sidebar_details(request):
    if request.user.is_authenticated():
        try:
            user_links = len(UserConnections.objects.filter(user=request.user))
        except:
            user_links = 0
        try:
            user_followers = len(UserConnections.objects.filter(connection=request.user))
        except:
            user_followers = 0
        return {'user_links': user_links, 'user_followers': user_followers}
    return {'user_links': 0, 'user_followers': 0}


def home_tutorial(request):
    if request.user.is_authenticated():
        try:
            Tutorial.objects.get(user=request.user)
            return {'tutorial': 1}
        except Tutorial.DoesNotExist:
            return {'tutorial': 0}
    return {'tutorial': 1}


def task1_badge(request):
    if request.user.is_authenticated():
        try:
            task1_badge = UserBadges.objects.filter(user=request.user)
            return {'task1_badge': task1_badge}
        except UserBadges.DoesNotExist:
            return {'task1_badge': 0}
    return {'task1_badge': 1}

