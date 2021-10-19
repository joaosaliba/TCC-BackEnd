from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from rede_social.models import Profile


class ProfileSerializer(serializers.Serializer):
    class meta:
        model:Profile
        fields = [
            'user',
            'bio',
            'birth_date',
            'picture',
            'location',
        ]


class ProfileGetSerializer(serializers.Serializer):

    class meta:
        model:Profile
        fields = [
            'user',
            'bio',
            'birth_date',
            'picture',
            'location',
        ]

