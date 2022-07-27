
from rede_auth.models import User
from rede_auth.permissions import IsSameUser
from rede_auth.views.mixed_view import MixedPermissionModelViewSet

from rede_social.models import Comments
from rede_social.pagination.LargeResultsSetPagination import StandardResultsSetPagination
from rede_social.serializers.comments_serializer import CommentsSerializer, CommentsGetSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.http import JsonResponse
from rest_framework.response import Response


class CommentsViewSet(MixedPermissionModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    pagination_class = StandardResultsSetPagination

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
                comments = Comments.objects.get(id=id)
                return self.queryset.filter(comments=comments)
        except TypeError as e:
            pass
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(commented_by=self.request.user)

    def get_serializer_class(self):
        # delete_users_and_channels()
        if self.request.method == "GET":
            return CommentsGetSerializer
        elif self.request.method in ['PUT', 'PATCH', 'POST']:
            return CommentsSerializer
        else:
            return CommentsGetSerializer

    def commetsOfPosts(self, request, pk=None):

        queryset = Comments.objects.filter(
            post_id=pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
