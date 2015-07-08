from userprofile.models import UserProfile

def check_profile(request):
    if request.user.is_authenticated():
        try:
            UserProfile.objects.get(user=request.user)
            return {'valid': 1}
        except UserProfile.DoesNotExist:
            return {'valid': 0, 'user_id': request.user.id}
    return {'valid': 1}
