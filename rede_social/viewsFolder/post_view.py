

from rede_auth.permissions import IsSameUser
from rede_auth.views.mixed_view import MixedPermissionModelViewSet
from rede_social.models import Post

from rede_social.serializers.post_serializer import PostSerializer, PostGetSerializer

from rest_framework.serializers import Serializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser


class PostViewSet(MixedPermissionModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [IsAuthenticated],
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
                post = Post.objects.get(id=id)
                return self.queryset.filter(post=post)
        except TypeError as e:
            pass
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_serializer_class(self):
        # delete_users_and_channels()
        if self.request.method == "GET":
            return PostGetSerializer
        elif self.request.method in ['PUT', 'PATCH', 'POST']:
            return PostSerializer
        else:
            return PostGetSerializer
