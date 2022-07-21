

from rede_auth.views.mixed_view import MixedPermissionModelViewSet
from rede_auth.permissions import IsSameUser
from rede_auth.models import User
from rede_social.models import Profile

from rest_framework.serializers import Serializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from rede_social.serializers.profile_serializer import ProfileGetSerializer, ProfileSerializer


class ProfileViewSet(MixedPermissionModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes_by_action = {
        'create': [IsAdminUser],
        'list': [AllowAny],
        'delete': [IsSameUser],
        'update': [IsSameUser],
        'partial_update': [IsSameUser]
    }

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        try:
            id = self.request.query_params.get('id', None)
            if id is not None:
                user = User.objects.get(id=id)
                return self.queryset.filter(user=user)
        except TypeError as e:
            pass
        return self.queryset

    def get_serializer_class(self):
        # delete_users_and_channels()
        if self.request.method == "GET":
            return ProfileGetSerializer
        elif self.request.method in ['PUT', 'PATCH', 'POST']:
            return ProfileSerializer
        else:
            return ProfileGetSerializer
