from django.conf.urls import include, url, patterns
from .views import artist_insights


urlpatterns = [
    url(r'^$', artist_insights, name='insights'),
]

