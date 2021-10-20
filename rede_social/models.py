from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import force_bytes
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from rede_auth.models import User
from django.conf import settings

import logging

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile', on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    
class Category(models.Model):
    name = models.CharField('Name', max_length=150)
    is_active = models.BooleanField(default=True)    

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return force_bytes('%s' % self.name)

    def __unicode__(self):
        return u'%s' % self.name

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=200)
    body = models.TextField(_('Body'), )
    reply_to = models.ForeignKey('self', blank=True, null=True, related_name='child', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL'), related_name='posts', on_delete=models.CASCADE)

    def __str__(self):
        # Use django.utils.encoding.force_bytes() because value returned is unicode
        return force_bytes('%s' % self.title)

    def __unicode__(self):
        return u'%s' % self.title

class Announcement(models.Model):
    title = models.CharField(_('Title'), max_length=200)
    body = models.TextField(_('Body'), )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL'), related_name='announcers', editable=False, on_delete=models.CASCADE)
    announce_from = models.DateTimeField(_('Announce from'), null=True, blank=True)
    announce_to = models.DateTimeField(_('Announce to'), null=True, blank=True)
    mark_as_read = models.ManyToManyField(getattr(settings, 'AUTH_USER_MODEL'), related_name='announcements',
                                          editable=False)

    class Meta:
        ordering = ['-created_at', ]

    def __str__(self):
        # Use django.utils.encoding.force_bytes() because value returned is unicode
        return force_bytes('%s' % self.title)

    def __unicode__(self):
        return u'%s' % self.title


class Following(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followed = models.ManyToManyField(User, related_name="followed")

    @classmethod
    def follow(cls, user, another_account):
        obj, create = cls.objects.get_or_create(user = user)
        obj.followed.add(another_account)
        pass

    @classmethod
    def unfollow(cls, user, another_account):
        obj, create = cls.objects.get_or_create(user = user)
        obj.followed.remove(another_account)

        pass

    def __str__(self):
        return str(self.user.username)