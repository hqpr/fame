from datetime import datetime

import pytz
from django.db import models
from django.contrib.auth.models import User
from apps.blog.models import PublishedManager, PublishedCommentManager


class ResourcesItemPublishedManager(models.Manager):
    def get_queryset(self):
        return super(ResourcesItemPublishedManager, self).get_queryset().\
            filter(resource_item__published=True, resource_item__publish_date__lte=datetime.now(tz=pytz.UTC))


class ResourcesItem(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    publish_date = models.DateTimeField()
    published = models.BooleanField(default=True)

    content = models.TextField()
    snippet = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to="resources/%y/%m/%d")
    cover_image = models.ImageField(upload_to="resources/%y/%m/%d")

    comments_open = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    objects = models.Manager()
    published_objects = PublishedManager()

    def __unicode__(self):
        return "%s" % self.title


class ResourcesAuthor(models.Model):
    resource_item = models.ForeignKey(ResourcesItem)
    author = models.ForeignKey(User)
    ordering = models.IntegerField()


class ResourcesCategory(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return "%s" % self.title


class ResourcesItemCategory(models.Model):
    resource_item = models.ForeignKey(ResourcesItem)
    resource_category = models.ForeignKey(ResourcesCategory)

    def __unicode__(self):
        return "%s" % self.resource_category.title


class ResourcesTag(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Tags"

    def __unicode__(self):
        return "%s" % self.title


class ResourcesItemTag(models.Model):
    resource_item = models.ForeignKey(ResourcesItem)
    resource_tag = models.ForeignKey(ResourcesTag)

    def __unicode__(self):
        return "%s" % self.resource_tag.title


class ResourcesItemComment(models.Model):
    resource_item = models.ForeignKey(ResourcesItem)
    user = models.ForeignKey(User)
    comment = models.TextField()
    reply_to = models.ForeignKey('self', blank=True, null=True, related_name="in_response_to")
    approved = models.BooleanField(default=False)
    created = models.DateTimeField()

    objects = models.Manager()
    published_objects = PublishedCommentManager()


class ResourcesCompetitionLinks(models.Model):
    resource_item = models.ForeignKey(ResourcesItem)
    competition = models.ForeignKey('competition.Competition')

    objects = models.Manager()
    published_objects = ResourcesItemPublishedManager()
