from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField

ACCOUNT_TYPES = (
    (1, 'Artist'),
    (2, 'Music Explorer'),
    (3, 'Music Industry'),
)


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    account_type = models.CharField(choices=ACCOUNT_TYPES, max_length=100)
    display_name = models.CharField(max_length=100)
    country = CountryField()
    picture = models.ImageField(upload_to='avatars')
    artist_name = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.user

