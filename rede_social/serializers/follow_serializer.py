from rede_social.models import Following
from rest_framework import serializers


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = [
            'user',
            'follow'
        ]
