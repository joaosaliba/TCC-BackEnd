from rest_framework import serializers
from rede_social.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'category',
            'body',
            'post_image',
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
