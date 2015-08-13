from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField
import datetime

ACCOUNT_TYPES = (
    ('1', 'Artist'),
    ('2', 'Muser'),
    ('3', 'Music Industry'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    account_type = models.CharField(choices=ACCOUNT_TYPES, max_length=100)
    display_name = models.CharField(max_length=100)
    birthday = models.DateField()
    country = CountryField()
    city = models.CharField(max_length=100, blank=True,null=True)
    picture = models.ImageField(upload_to='avatars/%y/%m/%d', blank=True, null=True)
    background_image = models.ImageField(upload_to='backgrounds/%y/%m/%d', blank=True, null=True)
    artist_name = models.CharField(max_length=100, blank=True, null=True)
    is_complete = models.BooleanField(default=False)
    language = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(default='')
    is_pro = models.BooleanField(default=False)
    about = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    genres = models.CharField(max_length=255, blank=True, null=True)
    influences = models.CharField(max_length=255, blank=True, null=True)
    artist_types = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.user_id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        return super(UserProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s" % self.user

class HallOfFame(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % (self.title,)


HALL_OF_FAME_TYPES = (
    ("winners", "Winners"),
    ("patrons", "Patrons"),
    ("sponsors", "Sponsors"),
)


class HallOfFameArtists(models.Model):
    hall_of_fame = models.ForeignKey(HallOfFame)
    user = models.OneToOneField(UserProfile)
    type = models.CharField(max_length=10,choices=HALL_OF_FAME_TYPES, default="winners")
    ordering = models.IntegerField()

    def __unicode__(self):
        return "%s: %s" % (self.hall_of_fame, self.user)


SOCIAL_ACCOUNTS = (
    ('instagram', 'Instagram'),
    ('twitter', 'twitter'),
    ('facebook', 'facebook'),
    ('youtube', 'youtube'),
    ('soundcloud', 'soundcloud'),
    ('wavo', 'wavo'),
    ('spotify', 'spotify'),
    ('vimeo', 'vimeo'),
)
class UserSocial(models.Model):
    user = models.ForeignKey(UserProfile)
    account = models.CharField(max_length=255, choices=SOCIAL_ACCOUNTS)
    link = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s: %s" % (self.user, self.account)
    

class UserStatus(models.Model):
    user = models.ForeignKey(UserProfile)
    status = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s: %s" % (self.user, self.status)


class UserGenre(models.Model):
    user = models.ForeignKey(UserProfile)
    genre = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s: %s" % (self.user, self.genre)


class UserInfluencer(models.Model):
    user = models.ForeignKey(UserProfile)
    influencer = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s: %s" % (self.user, self.influencer)


class UserTypes(models.Model):
    user = models.ForeignKey(UserProfile)
    type = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s: %s" % (self.user, self.type)
