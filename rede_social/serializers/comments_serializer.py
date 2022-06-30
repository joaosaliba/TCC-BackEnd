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
            'created_by',        
             
        ]

