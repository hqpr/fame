from .models import CompetitionChart

def competition_chart(request):
    if request.user.is_authenticated():
        try:
            CompetitionChart.objects.get(user=request.user)
            return {'valid': 1}
        except CompetitionChart.DoesNotExist:
            return {'valid': 0, 'user_id': request.user.id}
    return {'valid': 1}
