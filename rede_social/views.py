from django.db.models import query
from django.shortcuts import render
from rest_framework import viewsets
from rede_social.serializers.profile_serializer import ProfileGetSerializer, ProfileSerializer
from rede_auth.permissions import IsSameUser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from rede_social.models import Profile

# Create your views here.

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileGetSerializer
    permission_classes_by_action = {
        'create': [IsAdminUser],
        'list': [IsSameUser],
        'delete': [IsSameUser],
        'update': [IsSameUser],
        'partial_update': [IsSameUser]
    }

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        return self.queryset

    def get_serializer_class(self):
        # delete_users_and_channels()
        if self.request.method == "GET":
            return ProfileGetSerializer
        elif self.request.method in ['PUT', 'PATCH', 'POST']:
            return ProfileSerializer
        else:
            return ProfileGetSerializer