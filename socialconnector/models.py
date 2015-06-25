from django.db import models
from django.contrib.auth.models import User
from oauth2client.django_orm import FlowField, CredentialsField


class UserPhoto(models.Model):
    image = models.FileField(upload_to='photos')
    user = models.ForeignKey(User)
    added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.image

TRACK_CHOICES = (
    ('1', 'track_type_1'),
    ('2', 'track_type_2'),
    ('3', 'track_type_3'),
    ('4', 'track_type_4'),
)

GENRE_CHOICES = (
    ('rock', 'rock'),
    ('pop', 'pop'),
    ('classic', 'classic'),
)

PRIVACY_CHOICES = (
    ('private', 'private'),
    ('public', 'public'),
)


class UserAudio(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TRACK_CHOICES)
    genre = models.CharField(max_length=255, choices=GENRE_CHOICES, default='rock')
    description = models.TextField(blank=True, null=True)
    bpm = models.CharField(max_length=255, blank=True, null=True)
    privacy = models.CharField(max_length=255, choices=PRIVACY_CHOICES, default='public')
    audio = models.FileField(upload_to='audios')
    user = models.ForeignKey(User, default=1)
    added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    cover = models.FileField(upload_to='audios/covers', blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.title


class UserVideo(models.Model):
    video = models.FileField(upload_to='videos')
    user = models.ForeignKey(User)
    added = models.DateTimeField(auto_now_add=True)
    cover = models.FileField(upload_to='videos/covers', blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.video


class VideoPlaylist(models.Model):
    title = models.CharField(max_length=255)
    videos = models.ManyToManyField(UserVideo, blank=True, null=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return u'%s' % self.title
