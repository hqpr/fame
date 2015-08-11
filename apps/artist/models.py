from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Roles(models.Model):
    role = models.CharField(max_length=100)

    class Meta:
        db_table = "roles"

class UserRoles(models.Model):
    user = models.OneToOneField(User)
    roles = models.ManyToManyField(Roles)

    class Meta:
        db_table = "user_roles"

class UserConnections(models.Model):
    user = models.ForeignKey(User,related_name="follower")
    connection = models.ForeignKey(User,related_name="connection")

    class Meta:
        db_table = "user_connections"
        unique_together = ("user","connection")

    def clean(self):
        if self.user == self.connection:
            return False
        return

    def __unicode__(self):
        return "%s: %s" % (self.user, self.connection)

@receiver(post_save, sender=User)
def generate_user_roles(sender, instance, created, **kwargs):
    """Take user and generate roles if not existing"""
    try:
        UserRoles.objects.get(user=instance)
    except:
        user_roles = UserRoles(**{"user":instance})
        user_roles.save()
        user_roles.roles.add(1)
        user_roles.save()
