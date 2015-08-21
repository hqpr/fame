from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Conversation(models.Model):
    sender = models.ForeignKey(User, related_name="sender")
    receiver = models.ForeignKey(User, related_name="receiver")
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)


class Message(models.Model):
    conversation = models.ForeignKey(Conversation)
    sender = models.ForeignKey(User)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)