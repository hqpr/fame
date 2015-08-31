from datetime import datetime

from django.template.loader import render_to_string
from django.views.generic import FormView
import pytz
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
import simplejson

from apps.competition.models import Competition, CompetitionEntry, CompetitionEntryAudio, CompetitionStage, \
    CompetitionStageRequirement, CompetitionEntryVideo, CompetitionTerms
from apps.blog.models import BlogCompetitionLinks
from apps.media.models import Audio, Video
from apps.media.forms import AudioForm
from apps.userprofile.models import ConnectionFeed


def competitions(request, *args, **kwargs):
    """View all competitions"""
    # page setup
    filters = setup_competition_filters_dictionary(request.GET)

    # initial data setup
    # active competitions
    active_competitions = Competition.objects.filter(active=True,date_start__lte=datetime.now(tz=pytz.UTC),
                                                     date_end__gte=datetime.now(tz=pytz.UTC))
    # active_competitions = Competition.objects.filter(active=True,date_start__lte=datetime.now(tz=pytz.UTC))
    # set up pagination
    paginated_competitions = Paginator(active_competitions, filters["limit"])
    try:
        paginated_competitions_to_display = paginated_competitions.page(filters["page"])
    except:
        paginated_competitions_to_display = []

    # competition_tracks = CompetitionEntryAudio.objects.filter(competition_entry__competition=competition)

    template_name = 'competitions.html'
    template_data = {
        'competitions': active_competitions,
        "active_competitions": paginated_competitions_to_display,
        "string": "All Competitions Page",
        "paginator": paginated_competitions,
        'competition_tracks': True
    }

    return render_to_response(template_name,
                              template_data,
                              context_instance=RequestContext(request)
                              )

def single_competition(request, *args, **kwargs):
    """View single competition"""
    try:
        competition_slug = kwargs["slug"]
        competition = Competition.objects.get(slug=competition_slug)
    except:
        return HttpResponse("Error")

    competition_data = get_single_competition_data(competition, kwargs)

    judges = competition.competitionjudge_set.all()
    prizes = competition.competitionprize_set.all()
    try:
        terms = competition.competitionterms
    except:
        terms = ''
    terms_summary = competition.competitiontermsummary_set.all()
    countries = competition.competitioncountry_set.all()

    competition_tracks = CompetitionEntryAudio.objects.filter(competition_entry__competition=competition)[:3]

    try:
        access = CompetitionEntryAudio.objects.filter(entry=Audio.objects.filter(user=request.user),competition_entry__competition=competition)
    except:
        access = []

    latest_blog = ""
    latest_blog_list = BlogCompetitionLinks.published_objects.filter(competition=competition).order_by('-blog_item__publish_date')
    if len(latest_blog_list):
        latest_blog = latest_blog_list[0]

    template_name = competition_data["template_name"]
    template_data = {
        'prizes': prizes,
        'judges': judges,
        'terms': terms,
        'terms_summary': terms_summary,
        'countries': countries,
        'competition': competition,
        "page": competition_data["page"],
        "competition_tracks": competition_tracks,
        'access': access,
        'latest_blog': latest_blog
    }
    links = [rel.get_accessor_name() for rel in competition._meta.get_all_related_objects()]

    return render_to_response(template_name,
                              template_data,
                              context_instance=RequestContext(request)
                              )

def single_competition_terms(request, *args, **kwargs):
    """View single competition terms"""
    try:
        competition_slug = kwargs["slug"]
        competition = Competition.objects.get(slug=competition_slug)
    except:
        return HttpResponse("Error")

    try:
        terms = competition.competitionterms
    except:
        terms = ''

    template_name = "competition-terms.html"
    template_data = {
        'terms': terms
    }
    links = [rel.get_accessor_name() for rel in competition._meta.get_all_related_objects()]
    print links

    return render_to_response(template_name,
                              template_data,
                              context_instance=RequestContext(request)
                              )


class SingleCompetitionEnter(FormView):
    """Enter a given competitions"""
    template_name = 'enter-competition.html'
    form_class = AudioForm

    def get_context_data(self, **kwargs):
        context = super(SingleCompetitionEnter, self).get_context_data(**kwargs)
        tracks = Audio.objects.filter(user=self.request.user, is_complete=True)
        videos = Video.objects.filter(user=self.request.user, is_complete=True)
        competition = Competition.objects.get(slug=self.kwargs['slug'])
        access = CompetitionEntryAudio.objects.filter(entry=Audio.objects.filter(user=self.request.user))
        context.update({
            'competition': competition,
            'tracks': tracks,
            'videos': videos,
            'slug': self.kwargs['slug'],
            'access': access
        })
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.is_complete = True
        form.save()
        data = {
            'success': True,
            'slug': self.kwargs['slug']
        }
        ConnectionFeed.objects.create(user=self.request.user, action_type='entered_competition')
        print self.kwargs['slug'], 'here'
        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    def form_invalid(self, form):
        html = render_to_string(self.template_name, self.get_context_data(form=form))
        data = {
            'success': False,
            'forms': form.errors,
            'html': html
        }
        print html
        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    def render_to_response(self, context, **response_kwargs):
        return super(SingleCompetitionEnter, self).render_to_response(context, **response_kwargs)


def pick_media_file(request, *args, **kwargs):

    competition = Competition.objects.get(slug=kwargs["slug"])
    competition_stage = CompetitionStage.objects.filter(competition=competition, date_start__lte=datetime.now(tz=pytz.UTC), date_end__gte=datetime.now(tz=pytz.UTC))

    if not competition.active or not len(competition_stage) or not competition_stage[0].new_entries_open:
        return False

    if request.method == 'POST':
        try:
            entry = CompetitionEntry.objects.get(competition=competition, user=request.user)
        except:
            entry = CompetitionEntry(**{'competition':competition, 'user': request.user, 'name': request.user, 'final_points': 0, 'final_position': 0})
            entry.save()


        try:
            audio_id = request.POST['audio']
            competition_stage_requirement = CompetitionStageRequirement.objects.get(competition_stage=competition_stage[0], media_type="audio")
            if competition_stage_requirement:
                try:
                    audio = Audio.objects.get(id=int(audio_id),user=request.user)
                    CompetitionEntryAudio.objects.create(competition_entry=entry,
                                                         competition_stage_requirement=competition_stage_requirement,
                                                         entry=audio)
                    return HttpResponse(simplejson.dumps({'success': True}), content_type='application/json')
                except:
                    return HttpResponse(simplejson.dumps({'success': False}), content_type='application/json')
        except:
            video_id = request.POST.get('video', None)
            competition_stage_requirement = CompetitionStageRequirement.objects.get(competition_stage=competition_stage[0], media_type="video")
            try:
                print "HERE", video_id, competition_stage_requirement
                video = Video.objects.get(id=int(video_id),user=request.user)
                CompetitionEntryVideo.objects.create(competition_entry=entry,
                                                     competition_stage_requirement=competition_stage_requirement,
                                                     entry=video)
                return HttpResponse(simplejson.dumps({'success': True}), content_type='application/json')
            except:
                return HttpResponse(simplejson.dumps({'success': False}), content_type='application/json')

    tracks = Audio.objects.filter(user=request.user, is_complete=True)
    videos = Video.objects.filter(user=request.user, is_complete=True)

    template_name = 'enter-competition.html'
    template_data = {
        'competition': competition,
        'tracks': tracks,
        'videos': videos
    }

    return render_to_response(template_name,
                              template_data,
                              context_instance=RequestContext(request)
    )

"""
Supporting functions

The below are all functions to support the above views. They do not necessarily belong here and can be moved elsewhere if required
"""

"""
Functions for competitions view
"""

def setup_competition_filters_dictionary(dictionary):
    """Setup dictionary for competition based on filters

    Dictionary may, or may not, contain the following:
        c - country (2 character string)
        g - genre (list)
        l - list length (int, < 50)
        o - ordering (string)
        p - page (integer)
        q - search query (string)
    """
    #setup default dictionary
    temp_dictionary = {
        "page": 1,
        "genre": "",
        "country": "",
        "ordering": "",
        "title": "",
        "limit": 4
    }
    if "p" in dictionary:
        try:
            page = int(dictionary["p"])
            if page:
                temp_dictionary["page"] = page
        except:
            pass

    if "l" in dictionary:
        try:
            limit = int(dictionary["l"])
            if limit and limit < 50:
                temp_dictionary["limit"] = limit
        except:
            pass

    return temp_dictionary

"""
Functions for single competition view
"""

def get_single_competition_data(competition, kwargs):
    """Setup dictionary for single competition

    The data below changes based on different screens. The possibilities are:
        Overview (terms and conditions etc)
        Chart
        Single entry
    """
    # default dictionary
    temp_dictionary = {
        "page": "overview",
        "template_name": 'single-competition.html'
    }
    page_to_display = "overview"

    temp_dictionary["page"] = get_page_from_kwargs(kwargs)
    if temp_dictionary["page"] != "overview":
        temp_dictionary["template_name"] = 'single-competition-chart.html'

    return temp_dictionary

def get_page_from_kwargs(kwargs):
    """get display information from kwargs"""
    if not "display" in kwargs:
        return "overview"

    if kwargs["display"] == "chart":
        if "entry_slug" in kwargs:
            return "entry"
        return "chart"

    if kwargs["display"] == "terms":
        return "terms"

    return "overview"

def competition_add_audio(request, object_id):
    """
        Add uploaded audio to given competition.
        'slug' argument is on enter-competition.html data argument

    """
    if request.method == 'POST':
        slug = request.POST.get('slug', None)
        competition = Competition.objects.get(slug=slug)
        entry = CompetitionEntry.objects.get(competition=competition)
        competition_stage = CompetitionStage.objects.get(competition=competition)
        competition_stage_requirement = CompetitionStageRequirement.objects.get(competition_stage=competition_stage)
        audio = Audio.objects.get(id=int(object_id))
        CompetitionEntryAudio.objects.create(competition_entry=entry,
                                             competition_stage_requirement=competition_stage_requirement,
                                             entry=audio)

        return HttpResponse(simplejson.dumps({'success': True}), content_type='application/json')
    return HttpResponse(simplejson.dumps({'success': False}), content_type='application/json')

def competition_add_video(request, object_id):
    """
        Add uploaded audio to given competition.
        'slug' argument is on enter-competition.html data argument

    """
    if request.method == 'POST':
        slug = request.POST.get('slug', None)
        competition = Competition.objects.get(slug=slug)
        entry = CompetitionEntry.objects.get(competition=competition)
        competition_stage = CompetitionStage.objects.get(competition=competition)
        competition_stage_requirement = CompetitionStageRequirement.objects.get(competition_stage=competition_stage)
        video = Video.objects.get(id=int(object_id))
        CompetitionEntryVideo.objects.create(competition_entry=entry,
                                             competition_stage_requirement=competition_stage_requirement,
                                             entry=video)

        return HttpResponse(simplejson.dumps({'success': True}), content_type='application/json')
    return HttpResponse(simplejson.dumps({'success': False}), content_type='application/json')

def entry_review(request, slug):
    competition = Competition.objects.get(slug=slug)
    entry = CompetitionEntry.objects.get(competition=competition,user=request.user)
    try:
        audio_preview = CompetitionEntryAudio.objects.get(entry=Audio.objects.filter(user=request.user),
                                                          competition_entry=entry)
        video_preview = CompetitionEntryVideo.objects.get(entry=Video.objects.filter(user=request.user),
                                                          competition_entry=entry)
    except CompetitionEntryAudio.DoesNotExist or CompetitionEntryVideo.DoesNotExist:
        audio_preview = None
        video_preview = None
    terms = CompetitionTerms.objects.get(competition=competition)
    data = {'audio_preview': audio_preview,
            'video_preview': video_preview,
            'terms': terms}
    return render(request, 'entry-review.html', data)

