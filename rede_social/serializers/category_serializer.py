from unicodedata import category
from rest_framework import serializers
from rede_social.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name',
            'is_active'
        ]

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        category.save()
        return category

    def update(self, instance, validated_data):
        instance.save()
        return instance
