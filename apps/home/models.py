from django.contrib.auth.models import User
from django.db import models

class Tutorial(models.Model):
    user = models.OneToOneField(User)
    is_complete = models.NullBooleanField(default=False)

    def __unicode__(self):
        return "%s" % (self.user,)
