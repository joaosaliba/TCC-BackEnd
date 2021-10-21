from rest_framework import serializers
from rede_social.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'category', 
            'title', 
            'body', 
            'reply_to', 
            'created_at',
            'created_by', 
        ]



