from rest_framework import serializers
from rede_social.models import CommentLike


class CommentLikeSerializer(serializers.ModelSerializer):
    comment_disliked_by = serializers.ReadOnlyField(
        source='comment_disliked_by.email')
    comment_liked_by = serializers.ReadOnlyField(
        source='comment_liked_by.email')

    class Meta:
        model = CommentLike
        fields = [
            'id',
            'liked_comment',
            'comment_disliked_by',
            'comment_liked_by',
        ]
