from rest_framework import serializers
from rede_auth.serializers.user_serializer import UserToPostGetSerializer
from rede_social.models import Forms


class FormsSerializer(serializers.ModelSerializer):
    created_by = UserToPostGetSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Forms
        fields = [
            'id',
            'title',
            'link',
            'created_at',
            'created_by',
        ]
