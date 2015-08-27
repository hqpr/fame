from datetime import datetime

import pytz
from django.db import models
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(published=True,
                                                                   publish_date__lte=datetime.now(tz=pytz.UTC))


class BlogItemPublishedManager(models.Manager):
    def get_queryset(self):
        return super(BlogItemPublishedManager, self).get_queryset().\
            filter(blog_item__published=True, blog_item__publish_date__lte=datetime.now(tz=pytz.UTC))


class BlogItem(models.Model):
    """Model for blog"""
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    publish_date = models.DateTimeField()
    published = models.BooleanField(default=True)

    content = models.TextField()
    snippet = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to="blog/%y/%m/%d")
    cover_image = models.ImageField(upload_to="blog/%y/%m/%d")

    comments_open = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    objects = models.Manager()
    published_objects = PublishedManager()

    def __unicode__(self):
        return "%s" % self.title


class BlogAuthor(models.Model):
    blog_item = models.ForeignKey(BlogItem)
    author = models.ForeignKey(User)
    ordering = models.IntegerField()


class BlogCategory(models.Model):
    """Handle overall categories"""
    title = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255,unique=True,blank=True,null=True)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return "%s" % self.title


class BlogItemCategory(models.Model):
    """Handle Blog Categories"""
    blog_item = models.ForeignKey(BlogItem)
    blog_category = models.ForeignKey('blog.BlogCategory')

    def __unicode__(self):
        return "%s" % self.blog_category.title


class BlogTag(models.Model):
    """Handle overall categories"""
    title = models.CharField(max_length=255,unique=True)
    slug = models.CharField(max_length=255,unique=True,blank=True,null=True)

    class Meta:
        verbose_name_plural = "Tags"

    def __unicode__(self):
        return "%s" % self.title


class BlogItemTag(models.Model):
    """Handle Blog Categories"""
    blog_item = models.ForeignKey(BlogItem)
    blog_tag = models.ForeignKey(BlogTag)

    def __unicode__(self):
        return "%s" % self.blog_tag.title


class PublishedCommentManager(models.Manager):
    def get_queryset(self):
        return super(PublishedCommentManager, self).get_queryset().filter(approved=True)


class BlogItemComment(models.Model):
    """Handle Blog Item Comment"""
    blog_item = models.ForeignKey(BlogItem)
    user = models.ForeignKey(User)
    comment = models.TextField()
    reply_to = models.ForeignKey('self',blank=True,null=True,related_name="in_response_to")
    approved = models.BooleanField(default=False)
    created = models.DateTimeField()

    objects = models.Manager()
    published_objects = PublishedCommentManager()


class BlogCompetitionLinks(models.Model):
    """Handle blog competition link"""
    blog_item = models.ForeignKey(BlogItem)
    competition = models.ForeignKey('competition.Competition')

    objects = models.Manager()
    published_objects = BlogItemPublishedManager()