from django.conf.urls import url

from apps.competition.views import competitions, single_competition, single_competition_terms, pick_media_file, SingleCompetitionEnter, \
    competition_add_audio, competition_add_video, entry_review

urlpatterns = [
    url(r'^$', competitions, name='all_competitions'),
    url(r'^(?P<slug>[\w\-]+)/$', single_competition, {"display": "overview"}, name='single_competition'),
    url(r'^(?P<slug>[\w\-]+)/chart/$', single_competition, {"display": "chart"}, name='single_competition_chart'),
    url(r'^(?P<slug>[\w\-]+)/entry/(?P<entry_slug>[\w\-]+)$', single_competition, {"display": "chart"}, name='single_competition_entry'),
    url(r'^(?P<slug>[\w\-]+)/terms/$', single_competition_terms, {"display": "terms"}, name='single_competition_terms'),
    url(r'^(?P<slug>[\w\-]+)/enter/$', SingleCompetitionEnter.as_view(), name='single_competition_enter'),

    url(r'^(?P<slug>[\w\-]+)/pick/$', pick_media_file, name='pick_media_file'),
    url(r'^add/(?P<object_id>\d+)/$', competition_add_audio, name='competition_add_audio'),
    url(r'^add/video/(?P<object_id>\d+)/$', competition_add_video, name='competition_add_video'),
    url(r'^(?P<slug>[\w\-]+)/review/$', entry_review, name='entry_review'),
]
