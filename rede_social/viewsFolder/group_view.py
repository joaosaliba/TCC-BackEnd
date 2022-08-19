

from typing import List
from rede_auth.models import User
from rede_auth.permissions import IsTeacher
from rede_auth.views.mixed_view import MixedPermissionModelViewSet
from rede_social.models import Group
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from rede_social.serializers.group_serializer import GroupSerializer


class GroupViewSet(MixedPermissionModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [IsAuthenticated],
        'delete': [IsAuthenticated],
        'update': [IsAuthenticated],
        'partial_update': [IsAuthenticated]
    }

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        try:
            pk = self.request.query_params.get('pk', None)
            if pk is not None:
                group = Group.objects.get(pk=pk)
                return self.queryset.filter(group=group)
        except TypeError as e:
            pass
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def joinOrUnjoinGroup(self, request, pk):
        main_user = self.request.user
        particping_gropup = Group.objects.filter(
            id=pk, participants=main_user).exists()
        group = Group.objects.get(
            id=pk)
        queryset = Group.objects.filter(
            id=pk)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        if particping_gropup:
            Group.unjoin(group, main_user)
        else:
            Group.join(group, main_user)
        return self.get_paginated_response(serializer.data)
