from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from rede_social.models import Following, Profile
from rede_social.serializers.follow_serializer import FollowingGetSerializer, FollowingSerializer


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'bio',
            'birthdate',
            'location',
        ]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'user',
            'bio',
            'birthdate',
            'location',
        ]


class ProfileGetSerializer(serializers.ModelSerializer):
    followin_count = serializers.ReadOnlyField(
        source='get_follow_count', read_only=True)
    follower_count = serializers.ReadOnlyField(
        source='get_follower_count', read_only=True)
    follower = serializers.ListField(child=serializers.CharField(
        read_only=True), source='get_follows', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user',
            'bio',
            'birthdate',
            'location',
            'followin_count',
            'follower_count',
            'follower'
        ]
        extra_kwargs = {
            'follower': {'required': False},
        }
