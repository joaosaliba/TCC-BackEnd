from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from rede_social.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'user',
            'bio',
            'birth_date',
            'location',
        ]


class ProfileGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'user',
            'bio',
            'birth_date',
            'location',
        ]

