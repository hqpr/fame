from django.conf.urls import url

from apps.insights.views import artist_insights

urlpatterns = [
    url(r'^$', artist_insights, name='insights'),
]

