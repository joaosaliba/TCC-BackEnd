from rest_framework import serializers
from rede_social.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name',
            'is_active'
        ]