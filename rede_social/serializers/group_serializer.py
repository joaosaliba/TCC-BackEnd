from unicodedata import category
from rest_framework import serializers
from rede_auth.models import User
from rede_social.models import Category, Group

from rede_auth.serializers.user_serializer import UserToPostGetSerializer


class GroupSerializer(serializers.ModelSerializer):
    created_by = UserToPostGetSerializer(read_only=True)
    participants_count = serializers.ReadOnlyField(
        source='get_participants_count', read_only=True)
    participants = UserToPostGetSerializer(
        many=True, required=False)

    class Meta:
        model = Group
        fields = [
            'id',
            'title',
            'participants',
            'created_at',
            'created_by',
            'participants_count',
        ]
        extra_kwargs = {
            'created_by': {'required': False},
            'participants': {'required': False},
        }

    def validate(self, fields):
        if len(fields.get('title').strip()) < 1 or fields.get('title') == 'null':
            raise serializers.ValidationError(
                {'title': 'Um titulo do grupo deve ser preenchido.'})

        return fields

    def create(self, validated_data):
        group = Group.objects.create(**validated_data)
        section_user = validated_data['created_by']
        group.participants.add(section_user)
        group.save()
        return group

    def update(self, instance, validated_data):
        instance.save()
        return instance


class GroupGetSerializer(serializers.ModelSerializer):
    created_by = UserToPostGetSerializer(read_only=True)
    participants_count = serializers.ReadOnlyField(
        source='get_participants_count', read_only=True)

    class Meta:
        model = Group
        fields = [
            'id',
            'title',
            'participants',
            'created_at',
            'created_by',
            'participants_count',
        ]
        extra_kwargs = {
            'created_by': {'required': False},
            'participants': {'required': False},
        }
