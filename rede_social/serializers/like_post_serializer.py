from rest_framework import serializers
from rede_social.models import PostLike


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = [
            'liked',
            'liked_post',
            'liked_by',
        ]
