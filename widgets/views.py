from django.shortcuts import render


def trackcard(request):
    return render(request, 'widget-trackcard.html', {})