from unicodedata import category
from rest_framework import serializers
from rede_social.models import Category

from rede_auth.serializers.user_serializer import UserToPostGetSerializer


class CategorySerializer(serializers.ModelSerializer):
    created_by = UserToPostGetSerializer(read_only=True)
    participants_count = serializers.IntegerField(
        source='get_participants_count', read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'is_active',
            'created_at',
            'created_by',
            'participants_count',
        ]

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        category.save()
        return category

    def update(self, instance, validated_data):
        instance.save()
        return instance
