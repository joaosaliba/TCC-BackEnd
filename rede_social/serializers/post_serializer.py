from rede_auth.serializers.user_serializer import UserToPostGetSerializer
from rede_social.serializers.comments_serializer import CommentsGetSerializer
from rest_framework import serializers
from rede_social.models import Comments, Post


class PostSerializer(serializers.ModelSerializer):
    created_by = UserToPostGetSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            'category',
            'body',
            'post_image',
            'post_file',
            'reply_to',
            'created_at',
            'created_by',
        ]

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        post.save()
        return post

    def update(self, instance, validated_data):
        instance.save()
        return instance

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PostGetSerializer(serializers.ModelSerializer):
    created_by = UserToPostGetSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'category',
            'body',
            'post_image',
            'post_file',
            'reply_to',
            'created_at',
            'created_by',
        ]
