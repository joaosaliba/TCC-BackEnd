

from rede_auth.models import User
from rede_auth.permissions import IsTeacher
from rede_auth.views.mixed_view import MixedPermissionModelViewSet
from rede_social.models import Announcement
from rede_social.serializers.announcement_serializer import AnnouncementSerializer

from rest_framework.serializers import Serializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser


class AnnouncementViewSet(MixedPermissionModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes_by_action = {
        'create': [IsAdminUser, IsTeacher],
        'list': [AllowAny],
        'delete': [IsAdminUser],
        'update': [IsAdminUser],
        'partial_update': [IsAdminUser]
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
