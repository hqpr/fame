from django.core.exceptions import ValidationError
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
    uid = models.CharField(max_length=11,unique=True, blank=True,null=True)
    type = models.CharField(max_length=255, choices=TRACK_CHOICES, default=1)
    genre = models.ForeignKey(Genre, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    bpm = models.CharField(max_length=255, blank=True, null=True)
    privacy = models.CharField(max_length=255, choices=PRIVACY_CHOICES, default='public')
    audio = models.FileField(upload_to='audios/%y/%m/%d', default='default.mp3')
    added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    cover = models.FileField(upload_to='audios/covers/%y/%m/%d', blank=True, null=True)
    plays = models.IntegerField()
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
    uid = models.CharField(max_length=11,unique=True,blank=True, null=True)
    artist = models.CharField(max_length=255, default=None, blank=True, null=True)
    type = models.CharField(max_length=255, choices=TRACK_CHOICES, default=1)
    genre = models.ForeignKey(Genre, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    privacy = models.CharField(max_length=255, choices=PRIVACY_CHOICES, default='public')
    video = models.FileField(upload_to='videos/%y/%m/%d')
    added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    cover = models.FileField(upload_to='videos/covers/%y/%m/%d', blank=True, null=True)
    plays = models.IntegerField()
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
                video = Video.objects.get(uid=unique_key)
            except:
                break

        return unique_key

    def __unicode__(self):
        return "%s" % (self.name,)

    class Meta:
        db_table = "media_video"


class AudioPlaylist(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default=None)
    cover = models.ImageField(upload_to='playlists/%y/%m/%d', blank=True, null=True)
    user = models.ForeignKey(User)
    added = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __unicode__(self):
        return u'%s - %s' % (self.user, self.title)

    def files(self):
        return self.playlistitem_set.order_by('ordering')


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(AudioPlaylist)
    audio = models.ForeignKey(Audio)
    ordering = models.IntegerField()

    class Meta:
        db_table = "playlist_item"
        unique_together = ('playlist', 'audio',)


class AudioLike(models.Model):
    audio = models.ForeignKey(Audio)
    fan = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.fan:
            if self.fan == self.audio.user:
                raise ValidationError({"fan": "Cannot like your own track."})
        """Clean before saving"""
        if not self.is_unique_entry:
            raise ValidationError({"audio": "You have already liked this track"})

    def is_unique_entry(self):
        audio_like = AudioLike.objects.filter(audio=self.audio, fan=self.fan).exclude(id=self.id)
        if len(audio_like):
            return False
        return True

    def __unicode__(self):
        return "%s: %s" % (self.audio, self.fan)

    class Meta:
        db_table = "audio_likes"
        unique_together = ('audio', 'fan',)

class AudioComment(models.Model):
    audio = models.ForeignKey(Audio)
    fan = models.ForeignKey(User)
    comment = models.TextField()
    time_specific = models.BooleanField(default=False)
    time = models.IntegerField() # the time in seconds
    approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.fan:
            if self.fan == self.audio.user:
                raise ValidationError({"fan": "Cannot like your own track."})

    def __unicode__(self):
        return "%s: %s" % (self.audio, self.fan)

    class Meta:
        db_table = "audio_comments"