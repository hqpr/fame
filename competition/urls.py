from django.conf.urls import include, url
from django.contrib import admin

from competition.models import Competition
from competition.views import competitions, single_competition, pick_media_file, SingleCompetitionEnter, \
    competition_add_audio, competition_add_video

urlpatterns = [
    # Examples:
    # url(r'^$', 'fame.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', competitions, name='all_competitions'),
    url(r'^(?P<slug>[\w\-]+)/$', single_competition, {"display": "overview"}, name='single_competition'),
    url(r'^(?P<slug>[\w\-]+)/chart/$', single_competition, {"display": "chart"}, name='single_competition_chart'),
    url(r'^(?P<slug>[\w\-]+)/entry/(?P<entry_slug>[\w\-]+)$', single_competition, {"display": "chart"}, name='single_competition_entry'),
    url(r'^(?P<slug>[\w\-]+)/terms/$', single_competition, {"display": "terms"}, name='single_competition_terms'),
    url(r'^(?P<slug>[\w\-]+)/enter/$', SingleCompetitionEnter.as_view(), name='single_competition_enter'),

    url(r'^(?P<slug>[\w\-]+)/pick/$', pick_media_file, name='pick_media_file'),
    url(r'^add/(?P<object_id>\d+)/$', competition_add_audio, name='competition_add_audio'),
    url(r'^add/video/(?P<object_id>\d+)/$', competition_add_video, name='competition_add_video')
]
