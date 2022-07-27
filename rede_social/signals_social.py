from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rede_social.models import Profile


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()


post_save.connect(create_profile, sender=User)
