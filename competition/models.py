import pytz
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.crypto import get_random_string

from django_countries.fields import CountryField
from timezone_field import TimeZoneField

from media.models import Audio, Genre, Image, Video

"""
Root Competition class

This model document should contain all logic pertaining to Competitions. 

It has been built based on the UML document here: 
https://drive.draw.io/?#G0Bz67DiN00aOCd182VUx6cmJFcFk

The logic for the specification is outlined here:
https://docs.google.com/a/jbcole.co.uk/document/d/17SDFO1kyTrp-ARqj4CxJT4YiOCcmN8CQjesgc4P1WxE/edit#

Any changes to the model functionality need to be reflected in these two documents.
"""

# Create your models here.
class Competition(models.Model):
    """Parent class for complete competition"""
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=50,unique=True)
    timezone = TimeZoneField(default='Europe/London')
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    competition_page_image = models.ImageField(blank=True, null=True, upload_to="%y/%m/%d",verbose_name="Competition Image")
    competition_page_description = models.TextField(blank=True, null=True,verbose_name="Competition Description")
    judge_weighting = models.PositiveIntegerField(default=500)
    creator = models.ForeignKey(User)
    public = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    valid = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.id:
            if self.is_valid_competition():
                self.valid=True
            else:
                self.valid=False
        return

    def is_valid_competition(self):
        """Confirm this is a valid competition"""
        valid_competition_stage = self.has_valid_competition_stage()
        valid_competition_genre = self.has_valid_competition_genre()
        valid_competition_country = self.has_valid_competition_country()
        valid_competition_prize = self.has_valid_competition_prize()
        valid_competition_terms = self.has_valid_competition_terms()
        valid_competition_visuals = self.has_valid_competition_visuals()
        valid_competition_stage_primary = self.has_primary_competition_stage_requirement()
        if valid_competition_stage and valid_competition_genre and \
            valid_competition_country and valid_competition_prize and \
            valid_competition_terms and valid_competition_visuals and \
            valid_competition_stage_primary:
            return True
        return False

    def has_valid_competition_stage(self):
        try:
            CompetitionStage.objects.get(competition=self,final_stage=True)
            return True
        except:
            return False

    def has_valid_competition_genre(self):
        if len(CompetitionGenre.objects.filter(competition=self)) >= 1:
            return True
        return False

    def has_valid_competition_country(self):
        if len(CompetitionCountry.objects.filter(competition=self)) >= 1:
            return True
        return False

    def has_valid_competition_prize(self):
        if len(CompetitionPrize.objects.filter(competition=self)) >= 1:
            return True
        return False

    def has_valid_competition_terms(self):
        if len(CompetitionTerms.objects.filter(competition=self)) >= 1:
            return True
        return False

    def has_valid_competition_visuals(self):
        try:
            competition_visual = CompetitionVisual.objects.get(competition=self)
            if competition_visual.landing_page_content and \
                (competition_visual.landing_page_image or competition_visual.landing_page_video_url) and\
                competition_visual.entry_instructions:
                return True
        except:
            pass
        return False

    def has_number_entries(self):
        return len(CompetitionEntry.objects.filter(competition=self))

    def get_competition_status(self):
        current_datetime = datetime.now(tz=pytz.UTC)
        if current_datetime < self.date_start:
            return "not_started"
        if current_datetime > self.date_end:
            return "ended"
        if self.is_valid_competition():
            return "valid"
        return "invalid"

    def get_time_remaining(self):
        current_datetime = datetime.now(tz=self.timezone)
        if current_datetime > self.date_end:
            return 0

        time_remaining = self.date_end - current_datetime
        return time_remaining

    def has_primary_competition_stage_requirement(self):
        try:
            CompetitionStageRequirement.objects.get(competition_stage__competition=self,primary=True)
            return True
        except:
            pass

        return False

    def get_current_competition_stage(self):
        if timezone.now() < self.date_start:
            return None
        if timezone.now() > self.date_end:
            return None
        current_stage = CompetitionStage.objects.filter(date_start__lte=timezone.now()).order_by("-date_start")
        if len(current_stage):
            return current_stage[0]
        return None

    def time_until(self):
        now = datetime.now(timezone.utc)
        return now - self.date_end

    def __unicode__(self):
        return "%s" % self.name

    class Meta:
        db_table = "competitions"


class CompetitionCountry(models.Model):
    """Valid countries for Competitions"""
    competition = models.ForeignKey(Competition)
    country = CountryField()

    def __unicode__(self):
        return "%s: %s" % (self.competition,self.country)

    class Meta:
        db_table = "competition_countries"
        verbose_name_plural = "Competition countries"
        unique_together = ('competition', 'country',)


class CompetitionGenre(models.Model):
    """Competition Genres"""
    competition = models.ForeignKey(Competition)
    genre = models.ForeignKey(Genre)

    def __unicode__(self):
        return "%s: %s" % (self.competition,self.genre)

    class Meta:
        db_table = "competition_genres"
        unique_together = ('competition', 'genre',)


class CompetitionJudge(models.Model):
    """Competition Judge"""
    competition = models.ForeignKey(Competition)
    judge = models.ForeignKey(User)
    description = models.TextField()
    thumbnail_image = models.ImageField(upload_to="judges/thumbs/%y/%m/%d")
    carousel_image = models.ImageField(upload_to="judges/carousel/%y/%m/%d")
    ordering = models.PositiveIntegerField()

    def __unicode__(self):
        return "%s: %s" % (self.competition,self.judge)

    class Meta:
        db_table = "competition_judges"
        unique_together = ('competition', 'judge',)


class CompetitionPrize(models.Model):
    """Competition Prizes"""
    competition = models.ForeignKey(Competition)
    prize = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="prizes/%y/%m/%d")
    ordering = models.PositiveIntegerField()

    def __unicode__(self):
        return "%s: %s" % (self.competition,self.prize)

    class Meta:
        db_table = "competition_prizes"


class CompetitionTerms(models.Model):
    """Competition Terms"""
    competition = models.OneToOneField(Competition)
    terms = models.TextField()

    def __unicode__(self):
        return "%s: %s" % (self.competition,self.terms)

    class Meta:
        db_table = "competition_terms"
        verbose_name_plural = "Competition terms"


class CompetitionTermSummary(models.Model):
    """Competition Term Summaries

    For summarising on the single competition page"""
    competition = models.ForeignKey(Competition)
    term = models.TextField()
    ordering = models.PositiveIntegerField()

    def __unicode__(self):
        return "%s: %s" % (self.competition,self.term)

    class Meta:
        db_table = "competition_term_summaries"
        verbose_name_plural = "Competition terms - summaries"


class CompetitionVisual(models.Model):
    """Frontend visual features for Competition

    These are not required for all instances of the Competition so are kept separated"""
    competition = models.OneToOneField(Competition)
    landing_page_content = models.TextField(blank=True,null=True)
    landing_page_image = models.ImageField(blank=True,null=True,upload_to="%y/%m/%d")
    landing_page_video_url = models.CharField(max_length=255,blank=True,null=True)
    entry_instructions = models.TextField(blank=True,null=True)

    def __unicode__(self):
        return "%s" % self.competition

    class Meta:
        db_table = "competition_visuals"


"""
Partners

Partners may take more of a role in future so are setup in their own space
"""
class Partner(models.Model):
    """Partner"""
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="partners/%y/%m/%d")
    link = models.CharField(max_length=255,blank=True,null=True)

    def __unicode__(self):
        return "%s" % self.name

    class Meta:
        db_table = "partners"


class CompetitionPartner(models.Model):
    competition = models.ForeignKey(Competition)
    partner = models.ForeignKey(Partner)
    ordering = models.PositiveIntegerField()

    def __unicode__(self):
        return "%s: %s" % (self.competition, self.partner)

    class Meta:
        db_table = "competition_partners"
        unique_together = ("competition","partner")


"""
Stages

There is a lot of functionality linked with stages.

While there is an overall competition entry, it is the competition stage that ensures
the relevant media requirements have been fulfilled for a competition entry

Competition stages cannot:
    - overlap with each other
    - begin before the competition
    - end after the competition
    - can't be a knockout stage without a limit on entries
"""
class CompetitionStage(models.Model):
    """Competition Stage"""
    competition = models.ForeignKey(Competition)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    new_entries_open = models.BooleanField(default=False)
    voting_public = models.BooleanField(default=True, verbose_name="Public voting allowed")
    voting_judges = models.BooleanField(default=False, verbose_name="Judges voting allowed")
    knockout_stage = models.BooleanField(default=False)
    knockout_stage_limit = models.PositiveIntegerField(default=0)
    final_stage = models.BooleanField(default=False)
    ordering = models.PositiveIntegerField()

    def clean(self):
        if self.name:
            self.competition_stages_to_check = CompetitionStage.objects.filter(competition=self.competition).exclude(id=self.id)
            valid_date = self.is_valid_date_range()
            if valid_date['error']:
                raise ValidationError({valid_date['field']: valid_date['field_error']})

            if not self.confirm_valid_knockout_stage(self.knockout_stage, self.knockout_stage_limit):
                raise ValidationError({"knockout_stage": "You cannot assign a knockout stage without setting an entry limit"})

            if not self.confirm_valid_final_stage(self.final_stage, self.date_end, self.competition.date_end):
                raise ValidationError({"final_stage": "You can only assign a final stage to a stage that ends on the competition's final day"})

            valid_entries_access = self.is_valid_entries_access(self.new_entries_open)
            if valid_entries_access["error"]:
                raise ValidationError({"new_entries_open": valid_entries_access["field_error"]})

        return


    def is_valid_date_range(self):
        """Confirm date range within competition and not overlapping with other stages"""
        is_date_within_competition = self.is_date_within_competition()
        if is_date_within_competition['error']:
            return is_date_within_competition

        is_no_date_overlap = self.is_no_date_overlap()
        if is_no_date_overlap['error']:
            return is_no_date_overlap

        return {"error": False}
        

    def is_date_within_competition(self):
        """Confirm date range within competition"""
        if not self.date_is_bigger(self.date_start, self.competition.date_start, True):
            return {"error": True, "field": "date_start", "field_error": "Start date must be within competition date range"}
        if not self.date_is_bigger(self.competition.date_end, self.date_end, True):
            return {"error": True, "field": "date_end", "field_error": "End date must be within competition date range"}
        if not self.date_is_bigger(self.date_end, self.date_start, True):
            return {"error": True, "field": "date_start", "field_error": "Start date cannot be bigger than end date"}
        return {"error": False }

    def date_is_bigger(self, larger_date, smaller_date, equals=False):
        '''Confirm date is bigger'''
        # if equals, it matters if they overlap (e.g. start date and start date)
        if equals:
            if smaller_date >= larger_date:
                return False
        # if not equals, it doesn't matters if they overlap (e.g. end date and start date)
        if smaller_date > larger_date:
            return False
        return True

    def is_no_date_overlap(self):
        """Confirm date does not overlap with other competition stage"""
        if not len(self.competition_stages_to_check):
            return {"error": False }
        for stage in self.competition_stages_to_check:
            # check if start date overlaps with another competition stage
            if self.is_date_overlap(self.date_start, stage.date_start, stage.date_end, "start"):
                return {"error": True, "field": "date_start", "field_error": "Start date overlaps with another competition stage"}
            # check if end date overlaps with another competition stage
            if self.is_date_overlap(self.date_end, stage.date_start, stage.date_end, "end"):
                return {"error": True, "field": "date_end", "field_error": "End date overlaps with another competition stage"}
            # check if another competition stage start overlaps with this competition stage
            if self.is_date_overlap(stage.date_start, self.date_start, self.date_end):
                return {"error": True, "field": "date_start", "field_error": "Start date overlaps with another competition stage"}
            # check if another competition stage end overlaps with this competition stage
            if self.is_date_overlap(stage.date_end, self.date_start, self.date_end):
                return {"error": True, "field": "date_start", "field_error": "Start date overlaps with another competition stage"}
        return {"error": False }

    def is_date_overlap(self, date_to_check, start_date, end_date, overlap_type=None):
        if overlap_type and overlap_type == "start":
            if (self.date_is_bigger(date_to_check, start_date) or date_to_check == start_date) and self.date_is_bigger(end_date, date_to_check):
                return True
        elif overlap_type and overlap_type == "end":
            if self.date_is_bigger(date_to_check, start_date) and (self.date_is_bigger(end_date, date_to_check, True) or end_date == date_to_check):
                return True
        else:
            if self.date_is_bigger(date_to_check, start_date, True) and self.date_is_bigger(end_date, date_to_check, True):
                return True
        return False

    def confirm_valid_knockout_stage(self, is_knockout_stage, knockout_stage_participants):
        """Confirm valid knockout stage"""
        if is_knockout_stage and knockout_stage_participants < 1:
            return False
        return True

    def confirm_valid_final_stage(self, is_final_stage, stage_end_date, competition_end_date):
        """Confirm is a valid final stage"""
        if not is_final_stage:
            return True

        if stage_end_date.strftime("%Y-%m-%d") == competition_end_date.strftime("%Y-%m-%d"):
            return True

        return False

    def is_valid_entries_access(self, new_entries_open):
        """Check valid entry stage
        
        New entries can only be added in the first rounds of the Competition - must be adjoining
        """
        previous_competition_stages = CompetitionStage.objects.filter(date_start__lt=self.date_start, competition=self.competition)
        if not new_entries_open:
            # check if this is not the first competition stage
            if not len(previous_competition_stages):
                return {"error":True,"field_error":"Opening stages must be open for entries"}

        else:
            if self.knockout_stage:
                return {"error":True,"field_error":"Cannot allow open entries in a knockout stage"}
            if len(previous_competition_stages) and not previous_competition_stages[len(previous_competition_stages)-1].new_entries_open:
                return {"error":True,"field_error":"Cannot allow open entries this late in the competition"}

        return {"error":False}

    def __unicode__(self):
        return "%s: %s" % (self.competition, self.name)

    class Meta:
        db_table = "competition_stages"


REQUIREMENT_CHOICES = (
    ("audio", "Audio"),
    ("image", "Image"),
    ("video", "Video"),
)


class CompetitionStageRequirement(models.Model):
    """Competition Stage Requirement"""
    competition_stage = models.ForeignKey(CompetitionStage)
    name = models.CharField(max_length=255)
    description = models.TextField()
    media_type = models.CharField(max_length=10, choices=REQUIREMENT_CHOICES)
    total_required = models.PositiveIntegerField()
    primary = models.BooleanField(default=False)
    ordering = models.PositiveIntegerField()

    def clean(self):
        """Confirm this is all valid

        Media type is unique to Competition Stage
        """
        if not self.is_valid_media_type():
            raise ValidationError({"media_type":"Duplicate media type for this stage"})
        if not self.is_valid_competition_stage_requirement():
            raise ValidationError({"primary":"Error making this Competition Stage Requirement Primary"})
        return

    def is_valid_media_type(self):
        """Confirm the media type is valid"""
        competition_stage_requirements = CompetitionStageRequirement.objects.filter(competition_stage=self.competition_stage,media_type=self.media_type).exclude(id=self.id)
        if len(competition_stage_requirements):
            return False
        return True

    def is_valid_competition_stage_requirement(self):
        """Confirm is valid CSR"""
        if self.primary:
            if not self.is_unique_primary_requirement():
                return False
            if not self.has_unique_entry():
                return False
        return True

    def is_unique_primary_requirement(self):
        """Confirm is unique"""
        if not self.primary:
            return False

        primary_competition_stage_requirements = CompetitionStageRequirement.objects.filter(competition_stage__competition=self.competition_stage.competition,primary=True).exclude(id=self.id)
        if len(primary_competition_stage_requirements):
            return False
        return True

    def has_unique_entry(self):
        """Confirm has only one entry"""
        if self.total_required > 1:
            return False
        if self.total_required < 1:
            return False
        return True



    def __unicode__(self):
        return "%s: %s" % (self.competition_stage, self.name)

    class Meta:
        db_table = "competition_stage_requirements"
        unique_together = ("competition_stage","media_type")


"""
Competition Entry

Competition entries require comprehensive interaction
"""
class CompetitionEntry(models.Model):
    """Competition Entry"""
    competition = models.ForeignKey(Competition)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=False)
    knocked_out = models.BooleanField(default=False)
    knocked_out_date = models.DateField(blank=True,null=True)
    final_position = models.PositiveIntegerField()
    final_points = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    uid_string = models.CharField(unique=True, max_length=11, blank=True, null=True)

    def clean(self):
        if self.user:
            competition_judge = CompetitionJudge.objects.filter(competition=self.competition,judge=self.user)
            if len(competition_judge):
                raise ValidationError({"user": "Cannot create an entry if you are a judge."})
            if self.is_competition_creator():
                raise ValidationError({"user": "Cannot create an entry if you created the competitions."})
            if not self.is_unique_entry():
                raise ValidationError({"user": "You have already entered this competition."})
            if not self.can_create_entry():
                raise ValidationError({"user": "You cannot enter this competition."})
            if not self.uid_string:
                self.uid_string = self.generate_unique_string()
        return

    def generate_unique_string(self):
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        
        while True:
            unique_key = get_random_string(11, chars)

            try:
                competition_entry = CompetitionEntry.objects.get(uid_string=unique_key)
            except:
                break

        return unique_key

    def can_create_entry(self):
        if self.id:
            stages = CompetitionStage.objects.filter(competition=self.competition,date_start__lte=timezone.now(),date_end__gte=timezone.now())
        else:
            stages = CompetitionStage.objects.filter(competition=self.competition,date_start__lte=timezone.now(),date_end__gte=timezone.now(),new_entries_open=True)
        if len(stages):
            return True
        return False

    def is_valid_entry(self):
        """Confirm if is currently a valid entry"""
        now = timezone.now()
        stages = CompetitionStage.objects.filter(competition=self.competition,date_start__lte=now)
        requirements = CompetitionStageRequirement.objects.filter(competition_stage__in=[i for i in stages])
        entry_dictionary = {"audio":0,"image":0,"video":0}
        for requirement in requirements:
            entry_dictionary[requirement.media_type] += requirement.total_required

        audio_files = CompetitionEntryAudio.objects.filter(competition_entry=self)
        image_files = CompetitionEntryImage.objects.filter(competition_entry=self)
        video_files = CompetitionEntryVideo.objects.filter(competition_entry=self)

        if len(audio_files) >= entry_dictionary["audio"] \
            and len(image_files) >= entry_dictionary["image"] \
            and len(video_files) >= entry_dictionary["video"]:
            return "Yes"
        return "No"

    def is_competition_creator(self):
        """Check if user created competition"""
        try:
            Competition.objects.get(id=self.competition.id,creator=self.user)
            return True
        except:
            pass
        return False

    def is_unique_entry(self):
        """Check if this is a unique entry"""
        entry = CompetitionEntry.objects.filter(competition=self.competition,user=self.user).exclude(id=self.id)
        if len(entry):
            return False
        return True

    def __unicode__(self):
        return "%s: %s" % (self.competition, self.name)

    class Meta:
        db_table = "competition_entries"
        verbose_name_plural = "Competition Entries"
        unique_together = ("competition","user")

class CompetitionEntryAudio(models.Model):
    """Competition entry audio"""
    competition_entry = models.ForeignKey(CompetitionEntry)
    competition_stage_requirement = models.ForeignKey(CompetitionStageRequirement)
    entry = models.ForeignKey(Audio)

    def clean(self):
        """Clean before saving"""
        if not self.is_unique_entry:
            raise ValidationError({"entry": "You have already submitted that track"})

    def is_unique_entry(self):
        competition_audio = CompetitionEntryAudio.objects.filter(entry=self.entry).exclude(id=self.id)
        if len(competition_audio):
            return False
        return True

    def __unicode__(self):
        return "%s: %s" % (self.competition_entry, self.entry)

    class Meta:
        db_table = "competition_entry_audio"
        verbose_name_plural = "Competition Entry Audio"
        unique_together = ("competition_entry","entry")


class CompetitionEntryImage(models.Model):
    """Competition entry image"""
    competition_entry = models.ForeignKey(CompetitionEntry)
    competition_stage_requirement = models.ForeignKey(CompetitionStageRequirement)
    entry = models.ForeignKey(Image)

    def clean(self):
        """Clean before saving"""
        if not self.is_unique_entry:
            raise ValidationError({"entry": "You have already submitted that image"})

    def is_unique_entry(self):
        competition_image = CompetitionEntryImage.objects.filter(entry=self.entry).exclude(id=self.id)
        if len(competition_image):
            return False
        return True

    def __unicode__(self):
        return "%s: %s" % (self.competition_entry, self.entry)

    class Meta:
        db_table = "competition_entry_image"
        verbose_name_plural = "Competition Entry Image"
        unique_together = ("competition_entry","entry")


class CompetitionEntryVideo(models.Model):
    """Competition entry video"""
    competition_entry = models.ForeignKey(CompetitionEntry)
    competition_stage_requirement = models.ForeignKey(CompetitionStageRequirement)
    entry = models.ForeignKey(Video)

    def clean(self):
        """Clean before saving"""
        if not self.is_unique_entry:
            raise ValidationError({"entry": "You have already submitted that video"})

    def is_unique_entry(self):
        competition_video = CompetitionEntryVideo.objects.filter(entry=self.entry).exclude(id=self.id)
        if len(competition_video):
            return False
        return True

    def __unicode__(self):
        return "%s: %s" % (self.competition_entry, self.entry)

    class Meta:
        db_table = "competition_entry_video"
        verbose_name_plural = "Competition Entry Video"
        unique_together = ("competition_entry","entry")


class CompetitionEntryLike(models.Model):
    """Competition entry likes"""
    competition_entry = models.ForeignKey(CompetitionEntry)
    fan = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.fan:
            if self.fan == self.competition_entry.user:
                raise ValidationError({"fan": "Cannot like your own entry."})
            competition_judge = CompetitionJudge.objects.filter(judge=self.fan,competition=self.competition_entry.competition)
            if len(competition_judge):
                raise ValidationError({"fan": "Cannot like an entry if you are a judge."})
        """Clean before saving"""
        if not self.is_unique_entry:
            raise ValidationError({"competition_entry": "You have already liked this entry"})

    def is_unique_entry(self):
        competition_like = CompetitionEntryLike.objects.filter(competition_entry=self.competition_entry,fan=self.fan).exclude(id=self.id)
        if len(competition_like):
            return False
        return True


    def __unicode__(self):
        return "%s: %s" % (self.competition_entry, self.fan)

    class Meta:
        db_table = "competition_entry_likes"
        unique_together = ('competition_entry', 'fan',)

    def save(self, *args, **kwargs):
        print self.competition_entry, self.fan
        assert False
        super(CompetitionEntryLike).save(*args, **kwargs)


class CompetitionEntryComment(models.Model):
    """Competition entry comment"""
    competition_entry = models.ForeignKey(CompetitionEntry)
    fan = models.ForeignKey(User)
    comment = models.TextField()
    parent = models.ForeignKey("self",null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s: %s" % (self.competition_entry, self.comment)

    class Meta:
        db_table = "competition_entry_comments"


class CompetitionEntryRating(models.Model):
    """Competition entry comment"""
    competition_entry = models.ForeignKey(CompetitionEntry)
    judge = models.ForeignKey(CompetitionJudge)
    rating = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.judge:
            competition_judge = CompetitionJudge.objects.filter(judge=self.judge.judge,competition=self.competition_entry.competition)
            if not len(competition_judge):
                raise ValidationError({"judge": "Cannot rate an entry if you are not a judge."})
        if not self.is_unique_entry:
            raise ValidationError({"competition_entry": "You have already liked this entry"})

    def is_unique_entry(self):
        competition_entry_rating = CompetitionEntryRating.objects.filter(competition_entry=self.competition_entry,judge=self.judge).exclude(id=self.id)
        if len(competition_entry_rating):
            return False
        return True

    def __unicode__(self):
        return "%s: %s" % (self.competition_entry, self.judge)

    class Meta:
        db_table = "competition_entry_rating"
        unique_together = ('competition_entry', 'judge',)


# Extra classes

class CompetitionChart(models.Model):
    """Display competition chart

    This is a holding model that allows us to cache relevant ordering data"""
    entry = models.ForeignKey(CompetitionEntry,unique=True)
    current_score = models.PositiveIntegerField()
    plays = models.PositiveIntegerField()
    final = models.BooleanField(default=False)

    def create_chart(self, competition):
        """Create full chart based on Competition Stage"""
        current_entries = CompetitionChart.objects.filter(entry__competition=competition)
        if len(current_entries):
            return self.update_chart(competition)

        all_entries = CompetitionEntry.objects.filter(competition=competition)
        if len(all_entries):
            for entry in all_entries:
                self.create_entry(entry)
        return True

    def update_chart(self, competition):
        """Update chart

        Should be ongoing cron job. Needs to take into account:
            - Currently active competition stages
            - Currently active tracks + weighting"""
        if competition.closed:
            return

        competition_stage = competition.get_current_competition_stage()
        current_entries = CompetitionChart.objects.filter(entry__competition=competition)
        # if new entries available, update entries
        if competition_stage.new_entries_open:
            remaining_entries = CompetitionEntry.objects.filter(competition=competition).exclude(id__in=[i.entry.id for i in current_entries])
            if len(remaining_entries):
                for entry in remaining_entries:
                    self.create_entry(entry)
        
        for entry in current_entries:
            self.update_entry(entry)

        # if a knockout stage
        if competition_stage.knockout_stage:
            self.knockout_entries(competition, competition_stage.knockout_stage_limit)

        # if a final stage
        if competition_stage.final_stage and datetime.now(tz=pytz.UTC) > competition_stage.date_end:
            self.close_competition(competition)

        return True

    def close_competition(self, competition):
        """Close competition

        Should calculate final tallies and notify everyone that the chart has been secured.
        Should also notify winner and runners up if required."""
        self.knockout_entries(competition, 1)
        competition.closed = True
        competition.save()
        return True

    def knockout_entries(self, competition, limit):
        """Find which entries to knockout"""
        all_entries = CompetitionChart.objects.filter(entry__competition=competition).exclude(final=True).order_by('-current_score')
        if len(all_entries) > limit:
            knockout_entries = all_entries[limit:]
            for idx, entry in enumerate(knockout_entries):
                self.knockout_entry(entry,(idx+limit))
            return True
        return False

    def knockout_entry(self, entry, position):
        """Knocks out entry from competition

        Adds final score, final ranking to entry"""
        competition_entry = CompetitionEntry.objects.get(id=entry.entry.id)
        competition_entry.final_position=position
        competition_entry.knocked_out = True
        competition_entry.knocked_out_date = timezone.now()
        competition_entry.final_points = entry.current_score
        competition_entry.save()

        entry.final = True
        entry.save()
        return True


    def create_entry(self, entry):
        """Create entry

        On making a entry active in a competition, it becomes a permanent part of the competition"""
        current_score = self.calculate_score(entry)
        try:
            temp_entry = CompetitionChart(**{"entry":entry,"current_score":current_score,"plays":0})
            temp_entry.save()
            if temp_entry.id:
                return True
        except:
            pass
        return False

    def update_entry(self, entry):
        """Update single entry

        This should be called only when single entry needs updating"""
        if not entry.final:
            current_score = self.calculate_score(entry.entry)
            entry.current_score = current_score
            entry.save()
        return True

    def calculate_score(self, entry):
        """Calculate Score

        Takes likes and ratings and uses weightings to calculate them"""
        entry_likes = CompetitionEntryLike.objects.filter(competition_entry=entry).count()
        ratings = CompetitionEntryRating.objects.filter(competition_entry=entry)
        judge_weighting = entry.competition.judge_weighting

        temp_score = entry_likes
        if len(ratings):
            for rating in ratings:
                temp_score += self.return_judges_score(rating.rating, entry.competition.judge_weighting)
        return temp_score

    def return_judges_score(self, ranking, weighting):
        """Return judges score"""
        try:
            return ranking * weighting
        except:
            pass
        return 0

    def display_ranking(self, competition):
        """Display ranking for competition"""
        return CompetitionChart.objects.filter(entry__competition=competition).order_by('final','-current_score')

    def display_plays(self, competition):
        """Display by plays for competition"""
        return CompetitionChart.objects.filter(entry__competition=competition).order_by('-plays')

    def display_most_recent(self, competition):
        """Display by date created for competition"""
        return CompetitionChart.objects.filter(entry__competition=competition).order_by('-entry__created')



