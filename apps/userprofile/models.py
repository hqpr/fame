from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField
import datetime

ACCOUNT_TYPES = (
    ('1', 'Artist'),
    ('2', 'Muser'),
    ('3', 'Music Industry'),
)


FEED_TYPES = (
    ('uploaded_track', 'Uploaded a track'),
    ('uploaded_video', 'Uploaded a video'),
    ('playlist_created', 'Created a playlist'),
    ('entered_competition', 'Entered a competition'),
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
        if len(self.about) >= 300:
            try:
                s = Task1.objects.get(user=self.user)
                s.task1 = True
                s.save()
            except Task1.DoesNotExist:
                print '-'
                Task1.objects.create(user=self.user, task1=True)
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
    type = models.CharField(max_length=10, choices=HALL_OF_FAME_TYPES, default="winners")
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


class Badges(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='badges/')


class UserBadges(models.Model):
    user = models.ForeignKey(User)
    badge = models.ForeignKey(Badges)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge', )


class Task1(models.Model):
    user = models.ForeignKey(User)
    task1 = models.BooleanField(default=False)  # about >= 300
    task2 = models.BooleanField(default=False)  # audio file
    task3 = models.BooleanField(default=False)  # connect >= 3 social networks
    task4 = models.BooleanField(default=False)  # follow 3 artist
    task5 = models.BooleanField(default=False)  # video file

    def save(self, *args, **kwargs):
        if self.task1 and self.task2 and self.task3 and self.task4 and self.task5:
            UserBadges.objects.create(user=self.user, badge_id=1)
        return super(Task1, self).save(*args, **kwargs)


class ConnectionFeed(models.Model):
    user = models.ForeignKey(User)
    action_type = models.CharField(max_length=255, choices=FEED_TYPES)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s: %s" % (self.user, self.type)