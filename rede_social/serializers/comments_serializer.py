from rede_social.serializers.post_serializer import PostSerializer
from rest_framework import serializers
from rede_social.models import Comments


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = [
            'post',
            'comment',
            'comment_image',
            'reply_to',
            'created_at',
            'commented_by',

        ]


class CommentsGetSerializer(serializers.ModelSerializer):
    post = PostSerializer()

    class Meta:
        model = Comments
        fields = [
            'post',
            'comment',
            'comment_image',
            'reply_to',
            'created_at',
            'commented_by',

        ]
