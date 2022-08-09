from rede_social.models import Following
from rest_framework import serializers


class FollowingSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(read_only=True)

    class Meta:
        model = Following
        fields = [
            'user',
            'followin'
        ]


class FollowingGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Following
        fields = [
            'user',
            'follow'
        ]
