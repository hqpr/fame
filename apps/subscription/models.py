from django.contrib.auth.models import User
from django.db import models

class Subscription(models.Model):
    user = models.ForeignKey(User)
    amount = models.PositiveIntegerField()
    charge_date = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    email = models.EmailField()

    def __unicode__(self):
        return "%s" % (self.user,)