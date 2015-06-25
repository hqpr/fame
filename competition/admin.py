from django.contrib import admin
from django.forms import ModelForm

from suit.admin import SortableTabularInline
from suit_redactor.widgets import RedactorWidget

from .models import Competition, CompetitionCountry, CompetitionGenre, CompetitionJudge,\
                    CompetitionPartner, CompetitionPrize, CompetitionStage,\
                    CompetitionTermSummary, CompetitionTerms, CompetitionVisual,\
                    Partner, CompetitionStageRequirement, CompetitionEntry,\
                    CompetitionEntryAudio, CompetitionEntryImage, CompetitionEntryVideo,\
                    CompetitionEntryLike, CompetitionEntryComment, CompetitionEntryRating

from media.models import Audio, Image, Video

# Register your models here.
class CompetitionVisualForm(ModelForm):
    class Meta:
        widgets = {
            'landing_page_content': RedactorWidget(editor_options={'lang': 'en'})
        }

class CompetitionVisualInline(admin.TabularInline):
    """Competition visual"""
    model = CompetitionVisual

    form = CompetitionVisualForm
    fieldsets = [
      ('Body', {'classes': ('full-width',), 'fields': ('landing_page_content','landing_page_image','landing_page_video_url','entry_instructions')})
    ]

    suit_classes = 'suit-tab suit-tab-landing_page'

class CompetitionCountryInline(admin.TabularInline):
    """Competition Country"""
    model = CompetitionCountry
    suit_classes = 'suit-tab suit-tab-terms'


class CompetitionGenreInline(admin.TabularInline):
    """Competition Genre"""
    model = CompetitionGenre
    suit_classes = 'suit-tab suit-tab-genres'


class CompetitionJudgeInline(SortableTabularInline):
    """Competition Judge"""
    model = CompetitionJudge
    suit_classes = 'suit-tab suit-tab-judges'
    sortable = "ordering"


class CompetitionPartnerInline(SortableTabularInline):
    """Competition Prize"""
    model = CompetitionPartner
    suit_classes = 'suit-tab suit-tab-partners'
    sortable = "ordering"


class CompetitionPrizeInline(SortableTabularInline):
    """Competition Prize"""
    model = CompetitionPrize
    suit_classes = 'suit-tab suit-tab-prizes'
    sortable = "ordering"

class CompetitionStageInline(SortableTabularInline):
    """Competition Stages"""
    model = CompetitionStage
    suit_classes = 'suit-tab suit-tab-stages'
    sortable = "ordering"
    extra = 0

    readonly_fields = ['stage_link']

    fieldsets = [
        ('Body', {'fields': ('competition','name','description','date_start','date_end','voting_public','voting_judges','new_entries_open','knockout_stage','knockout_stage_limit','final_stage','ordering','stage_link')})
    ]

    def stage_link(self, obj):
        if obj:
            return "<a href='/sitepanel/competition/competitionstage/%s'>Link</a>" % (obj.id,)
        return ""

    stage_link.allow_tags = True


class TermSummaryForm(ModelForm):
    class Meta:
        widgets = {
            'term': RedactorWidget(editor_options={'lang': 'en'})
        }


class CompetitionTermSummaryInline(SortableTabularInline):
    """Competition Prize"""
    model = CompetitionTermSummary

    form = TermSummaryForm
    fieldsets = [
      ('Body', {'classes': ('full-width',), 'fields': ('term','ordering')})
    ]

    suit_classes = 'suit-tab suit-tab-terms'
    sortable = "ordering"


class TermsForm(ModelForm):
    class Meta:
        widgets = {
            'terms': RedactorWidget(editor_options={'lang': 'en'})
        }

class CompetitionTermsInline(admin.TabularInline):
    model = CompetitionTerms

    form = TermsForm
    fieldsets = [
      ('Body', {'classes': ('full-width',), 'fields': ('terms',)})
    ]

    suit_classes = 'suit-tab suit-tab-terms'


class CompetitionAdmin(admin.ModelAdmin):
    """Display Competition Admin"""
    model = Competition
    inlines = ()
    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = (CompetitionCountryInline, CompetitionGenreInline, CompetitionJudgeInline, CompetitionPartnerInline, CompetitionPrizeInline, CompetitionStageInline, CompetitionTermsInline, CompetitionTermSummaryInline, CompetitionVisualInline)
        self.suit_form_tabs = (('competition', 'Competition'), ('landing_page', 'Landing Page'),\
                      ('partners', 'Partners'), ('judges', 'Judges'), ('prizes', 'Prizes'), ('terms', 'Terms'),\
                      ('genres', 'Genres'), ('stages', 'Stages'))
        return super(CompetitionAdmin, self).change_view(request, object_id)

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = (CompetitionCountryInline, CompetitionGenreInline, CompetitionPartnerInline, CompetitionTermsInline, CompetitionTermSummaryInline, CompetitionVisualInline)
        self.suit_form_tabs = (('competition', 'Competition'), ('landing_page', 'Landing Page'),\
                      ('genres', 'Genres'))
        return super(CompetitionAdmin, self).add_view(request)

    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-competition',),
            'fields': ['name','slug','timezone','date_start','date_end','competition_page_image','competition_page_description','creator','public','active',]
        }),
    ]
    
    list_display = (
            "name",
            "valid",
            "valid_competition_stage",
            "has_valid_competition_genre",
            "has_valid_competition_country",
            "has_valid_competition_prize",
            "has_valid_competition_terms",
            "has_valid_competition_visuals",
            "has_primary_competition_stage_requirement"
        )

    def valid_competition_stage(self, obj):
        if obj.has_valid_competition_stage():
            return True
        return False

    def has_valid_competition_genre(self,obj):
        if obj.has_valid_competition_genre():
            return True
        return False

    def has_valid_competition_country(self, obj):
        if obj.has_valid_competition_country():
            return True
        return False

    def has_valid_competition_prize(self, obj):
        if obj.has_valid_competition_prize():
            return True
        return False

    def has_valid_competition_terms(self, obj):
        if obj.has_valid_competition_terms():
            return True
        return False

    def has_valid_competition_visuals(self, obj):
        if obj.has_valid_competition_visuals():
            return True
        return False

    def has_primary_competition_stage_requirement(self, obj):
        if obj.has_primary_competition_stage_requirement():
            return True
        return False

    def response_change(self, request, obj):
        if obj.is_valid_competition():
            obj.valid=True
        else:
            obj.valid=False
        obj.save()
        return super(CompetitionAdmin, self).response_change(request, obj)

    valid_competition_stage.boolean = True
    has_valid_competition_genre.boolean = True
    has_valid_competition_country.boolean = True
    has_valid_competition_prize.boolean = True
    has_valid_competition_terms.boolean = True
    has_valid_competition_visuals.boolean = True
    has_primary_competition_stage_requirement.boolean = True

    suit_form_tabs = (('competition', 'Competition'), ('landing_page', 'Landing Page'),\
                      ('partners', 'Partners'), ('judges', 'Judges'), ('prizes', 'Prizes'), ('terms', 'Terms'),\
                      ('genres', 'Genres'), ('stages', 'Stages'))



"""
Handle Partner
"""
class PartnerAdmin(admin.ModelAdmin):
    """Display Partners"""
    models = Partner


"""
Handle Competition Stage
"""
class CompetitionStageRequirementInline(SortableTabularInline):
    """Competition Stage Requirement"""
    model = CompetitionStageRequirement
    extra = 0

    suit_classes = 'suit-tab suit-tab-requirements'
    sortable = "ordering"


class CompetitionStageAdmin(admin.ModelAdmin):
    """Competition Stage"""
    model = CompetitionStage
    inlines = [CompetitionStageRequirementInline]

    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-competition_stage',),
            'fields': ['competition','name','description','date_start','date_end','voting_public','voting_judges','knockout_stage','knockout_stage_limit','final_stage','ordering','new_entries_open']
        }),
    ]

    suit_form_tabs = (('competition_stage', 'Competition Stage'), ('requirements', 'Requirements'))

"""
Handle Competition Entry
"""
class CompetitionEntryAudioInline(admin.TabularInline):
    """Competition Audio"""
    model = CompetitionEntryAudio
    suit_classes = 'suit-tab suit-tab-entries'
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "competition_stage_requirement":
            kwargs["queryset"] = CompetitionStageRequirement.objects.filter(media_type="audio")
        if db_field.name == "entry":
            try:
                kwargs["queryset"] = Audio.objects.filter(user=CompetitionEntry.objects.get(id=request.resolver_match.args[0]).user)
            except:
                kwargs["queryset"] = Audio.objects.all()
        return super(CompetitionEntryAudioInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class CompetitionEntryImageInline(admin.TabularInline):
    """Competition Image"""
    model = CompetitionEntryImage
    suit_classes = 'suit-tab suit-tab-entries'
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "competition_stage_requirement":
            kwargs["queryset"] = CompetitionStageRequirement.objects.filter(media_type="image")
        if db_field.name == "entry":
            try:
                kwargs["queryset"] = Image.objects.filter(user=CompetitionEntry.objects.get(id=request.resolver_match.args[0]).user)
            except:
                kwargs["queryset"] = Image.objects.all()
        return super(CompetitionEntryImageInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class CompetitionEntryVideoInline(admin.TabularInline):
    """Competition Video"""
    model = CompetitionEntryVideo
    suit_classes = 'suit-tab suit-tab-entries'
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "competition_stage_requirement":
            kwargs["queryset"] = CompetitionStageRequirement.objects.filter(media_type="video")
        if db_field.name == "entry":
            try:
                kwargs["queryset"] = Video.objects.filter(user=CompetitionEntry.objects.get(id=request.resolver_match.args[0]).user)
            except:
                kwargs["queryset"] = Video.objects.all()
        return super(CompetitionEntryVideoInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class CompetitionEntryLikeInline(admin.TabularInline):
    """Competition Like"""
    model = CompetitionEntryLike
    suit_classes = 'suit-tab suit-tab-likes'
    extra = 0


class CompetitionEntryCommentInline(admin.TabularInline):
    """Competition Comment"""
    model = CompetitionEntryComment
    suit_classes = 'suit-tab suit-tab-comments'
    extra = 0


class CompetitionEntryRatingInline(admin.TabularInline):
    """Competition Comment"""
    model = CompetitionEntryRating
    suit_classes = 'suit-tab suit-tab-ratings'
    extra = 0

class CompetitionEntryAdmin(admin.ModelAdmin):
    """Competition Entry"""
    model = CompetitionEntry

    readonly_fields = ['is_valid_entry']

    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-competition_entry',),
            'fields': ['competition','user','name','active','final_position','final_points','is_valid_entry','uid_string']
        }),
    ]

    def is_valid_entry(self, obj):
        if obj.id:
            return obj.is_valid_entry()
        return "No"

    is_valid_entry.allow_tags = True

    inlines = [CompetitionEntryAudioInline,CompetitionEntryImageInline,CompetitionEntryVideoInline,\
               CompetitionEntryCommentInline,CompetitionEntryRatingInline,CompetitionEntryLikeInline]
    suit_form_tabs = (('competition_entry', 'Competition Entry'), ('entries', 'Entries'),\
                      ('likes','Likes'),('comments','Comments'),('ratings','Ratings'))

admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(CompetitionStage, CompetitionStageAdmin)
admin.site.register(CompetitionEntry, CompetitionEntryAdmin)