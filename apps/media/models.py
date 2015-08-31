from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from mutagen.mp3 import MP3, HeaderNotFoundError
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to="genre/%y/%m/%d")

    def __unicode__(self):
        return "%s" % (self.name,)

    class Meta:
        db_table = "genre"

TRACK_CHOICES = (
    ('1', 'Single'),
    ('2', 'Album'),
    ('3', 'Remix'),
)

PRIVACY_CHOICES = (
    ('private', 'Private'),
    ('public', 'Public'),
)

class PublicManager(models.Manager):
    def get_queryset(self):
        return super(PublicManager, self).get_queryset().filter(privacy='public')


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
    audio = models.FileField(upload_to='audios/%y/%m/%d', default='default.mp3', )
    added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    cover = models.FileField(upload_to='audios/covers/%y/%m/%d', blank=True, null=True)
    plays = models.IntegerField(blank=True, null=True, default=0)
    is_complete = models.BooleanField(default=False)
    length = models.CharField(default=0, max_length=255, blank=True, null=True)
    soundcloud_track_id = models.CharField(max_length=255, blank=True, null=True)

    objects = models.Manager() # The default manager.
    public_objects = PublicManager()

    # def clean(self):
    #     if not self.uid:
    #         self.uid = self.generate_unique_string()
    #     return

    def generate_unique_string(self):
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        
        while True:
            unique_key = get_random_string(11, chars)

            try:
                Audio.objects.get(uid=unique_key)
            except Audio.DoesNotExist:
                break

        return unique_key

    def __unicode__(self):
        return "%s" % (self.name,)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.uid:
            self.uid = self.generate_unique_string()
        super(Audio, self).save(force_insert, force_update, using, update_fields)
        if self.length == 0:
            try:
                audio_file = MP3(self.audio.path)
            except HeaderNotFoundError:
                self.length = '-'
            else:
                m, s = divmod(audio_file.info.length, 60)
                h, m = divmod(m, 60)
                self.length = "%d:%02d:%02d" % (h, m, s)
            self.save()

    @property
    def likes(self):
        return len(AudioLike.objects.filter(audio=self))

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
    plays = models.IntegerField(blank=True, null=True, default=0)
    is_complete = models.BooleanField(default=False)

    objects = models.Manager() # The default manager.
    public_objects = PublicManager()

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
    time = models.CharField(max_length=255)  # the time in seconds
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

class VideoLike(models.Model):
    video = models.ForeignKey(Video)
    fan = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.fan:
            if self.fan == self.video.user:
                raise ValidationError({"fan": "Cannot like your own video."})
        """Clean before saving"""
        if not self.is_unique_entry:
            raise ValidationError({"video": "You have already liked this video"})

    def is_unique_entry(self):
        video_like = VideoLike.objects.filter(video=self.video, fan=self.fan).exclude(id=self.id)
        if len(video_like):
            return False
        return True

    def __unicode__(self):
        return "%s: %s" % (self.video, self.fan)

    class Meta:
        db_table = "video_likes"
        unique_together = ('video', 'fan',)

class VideoComment(models.Model):
    video = models.ForeignKey(Video)
    fan = models.ForeignKey(User)
    comment = models.TextField()
    time_specific = models.BooleanField(default=False)
    time = models.CharField(max_length=255)  # the time in seconds
    approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.fan:
            if self.fan == self.video.user:
                raise ValidationError({"fan": "Cannot comment on your own video."})

    def __unicode__(self):
        return "%s: %s" % (self.video, self.fan)

    class Meta:
        db_table = "video_comments"