from rede_auth.models import User
from rest_framework import serializers, routers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = [
            'id',
            'nome',
            'user_type',
            'email',
            'password',
            'password_confirmation',
            'old_password',
            'phonenumber',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirmation': {'write_only': True},
        }