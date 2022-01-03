import uuid
from typing import Coroutine
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):

    nome = models.CharField(_('name'), max_length=50, blank=True)
    email = models.EmailField(('email address'), unique=True)
    picture = models.FileField(
        _('picture'), blank=True, default='member-default.png')
    phonenumber = models.CharField(max_length=20, blank=True)
    password_confirmation = models.CharField(('password confirmation'), max_length=128)
    jwt_secret = models.UUIDField(default=uuid.uuid4)
    recipient_id = models.CharField(max_length=300, null=True)
    player_id = models.CharField(max_length=200, null=True)
    USER_TYPE_CHOICES = (
        ('Professor','Professor'),
        ('Aluno','Aluno'),
    )
    user_type = models.CharField(max_length=100, choices=USER_TYPE_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

User._meta.get_field('username')._unique = False


class Student(User):
    cpf = models.CharField(max_length=15, blank=True)
    consumer_external_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, blank=True)
    birthdate = models.DateField(auto_now=False, auto_now_add=False, default="1990-01-01", blank=True)
    class Meta:
        verbose_name = _('Aluno')
        verbose_name_plural = _('Aluno')


class Teacher(User):
    cpf = models.CharField(max_length=15, blank=True)
    consumer_external_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, blank=True)
    birthdate = models.DateField(auto_now=False, auto_now_add=False, default="1980-01-01", blank=True)
    class Meta:
        verbose_name = _('Professor')
        verbose_name_plural = _('Professor')