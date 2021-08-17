from typing import Coroutine
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):

    nome = models.CharField(_('name'), max_length=50, blank=True)
    email = models.EmailField(('email address'), unique=True)

    phonenumber = models.CharField(max_length=20, blank=True)
    passwordconfirmation = models.CharField(('password confirmation'), max_length=128)
    USER_TYPE_CHOICES = (
        ('Professor','Professor'),
        ('Aluno','Aluno'),
    )
    user_type = models.CharField(max_length=100, choices=USER_TYPE_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

User._meta.get_field('username')._unique = False
