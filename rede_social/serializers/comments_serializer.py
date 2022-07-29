from rede_auth.serializers.user_serializer import UserToPostGetSerializer
from rest_framework import serializers
from rede_social.models import Comments


class CommentsSerializer(serializers.ModelSerializer):
    commented_by = UserToPostGetSerializer(read_only=True)

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

    def create(self, validated_data):
        comment = Comments.objects.create(**validated_data)
        comment.save()
        return comment

    def update(self, instance, validated_data):
        instance.save()
        return instance


class CommentsGetSerializer(serializers.ModelSerializer):
    commented_by = UserToPostGetSerializer(read_only=True)
    dislikes_count = serializers.IntegerField(
        source='get_dislikes_count', read_only=True)
    likes_count = serializers.IntegerField(
        source='get_likes_count', read_only=True)

    class Meta:
        model = Comments
        fields = [
            'id',
            'comment',
            'comment_image',
            'reply_to',
            'created_at',
            'commented_by',
            'post',
            'dislikes_count',
            'likes_count'

        ]
