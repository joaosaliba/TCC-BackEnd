from numpy import empty, source
from rede_auth.serializers.user_serializer import UserToPostGetSerializer
from .category_serializer import CategorySerializer
from rede_social.serializers.comments_serializer import CommentsGetSerializer
from rest_framework import serializers
from rede_social.models import Comments, Post, PostLike


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
        extra_kwargs = {
            'category': {'required': False}
        }

    def validate(self, fields):
        if len(fields.get('body').strip()) < 1 or fields.get('body') == 'null':
            raise serializers.ValidationError(
                {'body': 'A mensagem do post deve ser preenchido.'})
        return fields

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
    likes_count = serializers.IntegerField(
        source='get_likes_count', read_only=True)
    dislikes_count = serializers.IntegerField(
        source='get_dislikes_count', read_only=True)
    comments_count = serializers.IntegerField(
        source='get_comments_count', read_only=True)
    category = CategorySerializer(read_only=True)

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
            'likes_count',
            'dislikes_count',
            'comments_count'
        ]
        extra_kwargs = {
            'category': {'required': False}
        }
