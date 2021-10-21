from rest_framework import serializers
from rede_social.models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = [
            'title',
            'body',
            'created_at' ,
            'created_by',
            'announce_from',
            'announce_to',
            'mark_as_read', 
        ]


