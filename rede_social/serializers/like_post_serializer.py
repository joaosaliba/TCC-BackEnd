from rest_framework import serializers
from rede_social.models import PostLike


class PostLikeSerializer(serializers.ModelSerializer):
    disliked_by = serializers.ReadOnlyField(source='disliked_by.email')
    liked_by = serializers.ReadOnlyField(source='liked_by.email')

    class Meta:
        model = PostLike
        fields = [
            'id',
            'liked_post',
            'disliked_by',
            'liked_by',
        ]
