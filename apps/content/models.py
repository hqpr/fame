from django.db import models

# Create your models here.
class FaqItem(models.Model):
    """Handle FAQ Item"""
    question = models.TextField()
    answer = models.TextField()

class Question(models.Model):
    """Handle FAQ Item"""
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    question = models.TextField()