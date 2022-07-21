from rede_auth.serializers.user_serializer import UserToPostGetSerializer
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
    commented_by = UserToPostGetSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = [
            'comment',
            'comment_image',
            'reply_to',
            'created_at',
            'commented_by',

        ]
