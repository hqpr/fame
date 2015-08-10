from userprofile.models import UserProfile
from artist.models import UserConnections

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