from __future__ import unicode_literals
from tkinter import CASCADE
from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import force_bytes
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from rede_auth.models import User
from django.conf import settings
from django_currentuser.db.models import CurrentUserField

import logging

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, related_name='profile', on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, blank=True, null=True)
    birthdate = models.DateField(
        auto_now=False, auto_now_add=False, default="1990-01-01", blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    follows = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False, blank=True
    )

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField('Name', max_length=150)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(_('Body'), null=False, blank=False)
    post_image = models.ImageField(_('post_image'), blank=True)
    reply_to = models.ForeignKey(
        'self', blank=True, null=True, related_name='child', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = CurrentUserField(
        related_name='created_by', on_delete=models.CASCADE)


class Comments(models.Model):
    post = models.ForeignKey(
        Post, related_name='post_comment', on_delete=models.CASCADE)
    comment = models.CharField(max_length=4000)
    comment_image = models.ImageField(null=True, blank=True)
    reply_to = models.ForeignKey(
        'self', blank=True, null=True, related_name='post_reply', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    commented_by = CurrentUserField(
        related_name='commented_by', on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['-created_at', ]


class PostLike(models.Model):
    liked = models.BooleanField(null=True)
    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_by = CurrentUserField(
        related_name='postlike', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.liked_post)


class Announcement(models.Model):
    title = models.CharField(_('Title'), max_length=200)
    body = models.TextField(_('Body'), )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = CurrentUserField(
        related_name='announcers', editable=False, on_delete=models.CASCADE)
    announce_from = models.DateTimeField(
        _('Announce from'), null=True, blank=True)
    announce_to = models.DateTimeField(_('Announce to'), null=True, blank=True)
    mark_as_read = models.ManyToManyField(getattr(settings, 'AUTH_USER_MODEL'), related_name='announcements',
                                          editable=False)

    class Meta:
        ordering = ['-created_at', ]


class Following(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followed = models.ManyToManyField(User, related_name="followed")

    @classmethod
    def follow(cls, user, another_account):
        obj, create = cls.objects.get_or_create(user=user)
        obj.followed.add(another_account)
        pass

    @classmethod
    def unfollow(cls, user, another_account):
        obj, create = cls.objects.get_or_create(user=user)
        obj.followed.remove(another_account)

        pass

    def __str__(self):
        return str(self.user.username)
