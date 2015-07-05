from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogItem(models.Model):
    """Model for blog"""
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    publish_date = models.DateField(auto_now=True)
    published = models.BooleanField(default=True)

    content = models.TextField()
    snippet = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to="blog/%y/%m/%d")
    cover_image = models.ImageField(upload_to="blog/%y/%m/%d")

    comments_open = models.BooleanField(default=True)


class BlogAuthor(models.Model):
    blog_item = models.ForeignKey(BlogItem)
    author = models.ForeignKey(User)
    ordering = models.IntegerField()

class BlogCategory(models.Model):
    """Handle overall categories"""
    title = models.CharField(max_length=255,unique=True)


class BlogItemCategory(models.Model):
    """Handle Blog Categories"""
    blog_item = models.ForeignKey(BlogItem)
    blog_category = models.ForeignKey(BlogCategory)

class BlogTag(models.Model):
    """Handle overall categories"""
    title = models.CharField(max_length=255,unique=True)

class BlogItemTag(models.Model):
    """Handle Blog Categories"""
    blog_item = models.ForeignKey(BlogItem)
    blog_tag = models.ForeignKey(BlogTag)

class BlogItemComment(models.Model):
    """Handle Blog Item Comment"""
    blog_item = models.ForeignKey(BlogItem)
    user = models.ForeignKey(User)
    comment = models.TextField()
    reply_to = models.ForeignKey('self',blank=True,null=True,related_name="in_response_to")