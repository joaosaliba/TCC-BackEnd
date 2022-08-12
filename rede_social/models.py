from __future__ import unicode_literals
from tkinter import CASCADE
from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import force_bytes
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from rede_auth.models import User
from django.conf import settings
from django.db.models import Count
import logging

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, related_name='profile', on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, blank=True, null=True)
    birthdate = models.DateField(
        auto_now=False, auto_now_add=False, default="1990-01-01", blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_follow_count(self):
        return Following.objects.filter(user=self.user).count()

    def get_follower_count(self):
        return Following.objects.filter(followin=self.user).count()

    def get_follows(self):
        follows = Following.objects.filter(
            followin=self.user)
        return follows

    def get_followin(self):
        followin = Following.objects.filter(
            user=self.user)
        return followin


class Following(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followin = models.ManyToManyField(User, related_name="followin")

    @classmethod
    def follow(cls, user, another_account):
        obj, create = cls.objects.get_or_create(user=user)
        obj.followin.add(another_account)
        pass

    @classmethod
    def unfollow(cls, user, another_account):
        obj, create = cls.objects.get_or_create(user=user)
        obj.followin.remove(another_account)

    class Meta:
        verbose_name = 'Following'
        verbose_name_plural = 'Following'

    def __str__(self):
        return str(self.user.email)


class Category(models.Model):
    name = models.CharField('Name', max_length=150, default="feed")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(getattr(
        settings, 'AUTH_USER_MODEL'),
        related_name='category_created_by', default=None, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def get_participants_count(self):
        user_count = Post.objects.distinct().filter(
            category=self.pk).values('created_by').count()
        # user.annotate(
        #     user_count=Count('created_by', distinct=True))

        return user_count

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=None, null=True, blank=True)
    body = models.TextField(_('body'), null=False, blank=False)
    post_image = models.ImageField(_('post_image'), blank=True)
    post_file = models.FileField(_('post_file'), blank=True)
    reply_to = models.ForeignKey(
        'self', blank=True, null=True, related_name='child', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(getattr(
        settings, 'AUTH_USER_MODEL'),
        related_name='created_by', on_delete=models.CASCADE)

    def get_user(self):
        user = vars(self.created_by)
        return {"id": user["id"], "email": user["email"]}

    def get_likes_count(self):
        return PostLike.objects.filter(disliked_by=None, liked_post=self).count()

    def get_dislikes_count(self):
        return PostLike.objects.filter(liked_by=None, liked_post=self).count()

    def get_comments(self):
        return Comments.objects.filter(post=self.pk)

    def get_comments_count(self):
        return Comments.objects.filter(post=self.pk).count()

    def __str__(self):
        return self.body

    class Meta:
        ordering = ['-created_at', ]


class Comments(models.Model):
    post = models.ForeignKey(
        Post, related_name='post_comment', on_delete=models.CASCADE)
    comment = models.CharField(max_length=4000)
    comment_image = models.ImageField(
        _('comment_image'), null=True, blank=True)
    reply_to = models.ForeignKey(
        'self', blank=True, null=True, related_name='comment_reply', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    commented_by = models.ForeignKey(getattr(
        settings, 'AUTH_USER_MODEL'),
        related_name='commented_by', on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

    def get_likes_count(self):
        return CommentLike.objects.filter(comment_disliked_by=None, liked_comment=self).count()

    def get_dislikes_count(self):
        return CommentLike.objects.filter(comment_liked_by=None, liked_comment=self).count()

    class Meta:
        ordering = ['-created_at', ]


class CommentLike(models.Model):
    liked_comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    comment_liked_by = models.ForeignKey(getattr(
        settings, 'AUTH_USER_MODEL'),
        related_name='comment_liked_by', on_delete=models.CASCADE,  default=None, blank=True, null=True)
    comment_disliked_by = models.ForeignKey(getattr(
        settings, 'AUTH_USER_MODEL'), related_name='comment_disliked_by', on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return str(self.liked_post)


class PostLike(models.Model):
    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(getattr(
        settings, 'AUTH_USER_MODEL'),
        related_name='liked_by', on_delete=models.CASCADE,  default=None, blank=True, null=True)
    disliked_by = models.ForeignKey(getattr(
        settings, 'AUTH_USER_MODEL'), related_name='disliked_by', on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return str(self.liked_post)


class Announcement(models.Model):
    title = models.CharField(_('Title'), max_length=200)
    body = models.TextField(_('Body'), )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(getattr(
        settings, 'AUTH_USER_MODEL'),
        related_name='announcers', editable=False, on_delete=models.CASCADE)
    announce_from = models.DateTimeField(
        _('Announce from'), null=True, blank=True)
    announce_to = models.DateTimeField(_('Announce to'), null=True, blank=True)
    mark_as_read = models.ManyToManyField(getattr(settings, 'AUTH_USER_MODEL'), related_name='announcements',
                                          editable=False)

    class Meta:
        ordering = ['-created_at', ]
