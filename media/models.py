from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


class Genre(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to="genre/%y/%m/%d")

    def __unicode__(self):
        return "%s" % (self.name,)

    class Meta:
        db_table = "genre"

TRACK_CHOICES = (
    ('1', 'Single'),
    ('2', 'Ketchup'),
    ('3', 'Relish'),
)

PRIVACY_CHOICES = (
    ('private', 'private'),
    ('public', 'public'),
)

class Audio(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    artist = models.CharField(max_length=255, default=None, blank=True, null=True)
    uid = models.CharField(max_length=11,unique=True,blank=True,null=True)
    type = models.CharField(max_length=255, choices=TRACK_CHOICES, default=1)
    genre = models.ForeignKey(Genre, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    bpm = models.CharField(max_length=255, blank=True, null=True)
    privacy = models.CharField(max_length=255, choices=PRIVACY_CHOICES, default='public')
    audio = models.FileField(upload_to='audios/%y/%m/%d', default='default.mp3')
    added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    cover = models.FileField(upload_to='audios/covers/%y/%m/%d', blank=True, null=True)
    is_complete = models.BooleanField(default=False)

    def clean(self):
        if not self.uid:
            self.uid = self.generate_unique_string()
        return

    def generate_unique_string(self):
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        
        while True:
            unique_key = get_random_string(11, chars)

            try:
                audio = Audio.objects.get(uid=unique_key)
            except:
                break

        return unique_key

    def __unicode__(self):
        return "%s" % (self.name,)

    class Meta:
        db_table = "media_audio"


class Image(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    uid = models.CharField(max_length=11,unique=True,blank=True,null=True)

    def clean(self):
        if not self.uid:
            self.uid = self.generate_unique_string()
        return

    def __unicode__(self):
        return "%s" % (self.name,)

    def generate_unique_string(self):
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        
        while True:
            unique_key = get_random_string(11, chars)

            try:
                image = Image.objects.get(uid=unique_key)
            except:
                break

        return unique_key

    class Meta:
        db_table = "media_image"


class Video(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    uid = models.CharField(max_length=11,unique=True,blank=True,null=True)

    def clean(self):
        if not self.uid:
            self.uid = self.generate_unique_string()
        return

    def generate_unique_string(self):
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        
        while True:
            unique_key = get_random_string(11, chars)

            try:
                video = Video.objects.get(uid=unique_key)
            except:
                break

        return unique_key

    def __unicode__(self):
        return "%s" % (self.name,)

    class Meta:
        db_table = "media_video"


class VideoPlaylist(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, default=None)
    genre = models.ForeignKey(Genre, default=1)
    privacy = models.CharField(max_length=100, default=None)
    description = models.TextField(default=None)
    cover = models.ImageField(upload_to='playlists/%y/%m/%d', blank=True, null=True)
    videos = models.ManyToManyField(Video, blank=True, null=True)
    user = models.ForeignKey(User)
    added = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __unicode__(self):
        return u'%s - %s' % (self.user, self.title)
