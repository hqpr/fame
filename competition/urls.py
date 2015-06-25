from django.conf.urls import include, url
from django.contrib import admin

from competition.models import Competition
from competition.views import competitions, single_competition, single_competition_enter

urlpatterns = [
    # Examples:
    # url(r'^$', 'fame.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', competitions, name='all_competitions'),
    url(r'^(?P<slug>[\w\-]+)/$', single_competition, {"display":"overview"}, name='single_competition'),
    url(r'^(?P<slug>[\w\-]+)/chart/$', single_competition, {"display":"chart"}, name='single_competition_chart'),
    url(r'^(?P<slug>[\w\-]+)/entry/(?P<entry_slug>[\w\-]+)$', single_competition, {"display":"chart"}, name='single_competition_entry'),
    url(r'^(?P<slug>[\w\-]+)/terms/$', single_competition, {"display":"terms"}, name='single_competition_terms'),
    url(r'^(?P<slug>[\w\-]+)/enter/$', single_competition_enter, name='single_competition_enter'),
]
