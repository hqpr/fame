from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField
import datetime

ACCOUNT_TYPES = (
    ('1', 'Artist'),
    ('2', 'Music Explorer'),
    ('3', 'Music Industry'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    account_type = models.CharField(choices=ACCOUNT_TYPES, max_length=100)
    display_name = models.CharField(max_length=100)
    birthday = models.DateField(default=datetime.datetime.now())
    country = CountryField()
    picture = models.ImageField(upload_to='avatars', blank=True, null=True)
    artist_name = models.CharField(max_length=100, blank=True, null=True)
    is_complete = models.BooleanField(default=False)
    created = models.DateTimeField(editable=False, default=datetime.datetime.now())
    modified = models.DateTimeField(default=datetime.datetime.now())

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        return super(UserProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s" % self.user

