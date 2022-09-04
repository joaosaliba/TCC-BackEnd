

from urllib import request
from xmlrpc.client import Boolean
from rede_auth.models import User
from rede_auth.permissions import IsSameUser
from rede_auth.views.mixed_view import MixedPermissionModelViewSet
from rede_social.models import Following, Post, Profile
from rede_social.pagination.LargeResultsSetPagination import LargeResultsSetPagination, StandardResultsSetPagination

from rede_social.serializers.post_serializer import PostSerializer, PostGetSerializer

from rest_framework.serializers import Serializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from django.db.models import Q
from datetime import date, timedelta
from django.db.models import Count
from django.utils import timezone


class PostViewSet(MixedPermissionModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
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
        category = self.request.query_params.get('category', None)
        if category is not None:
            return self.queryset.filter(category=category)
        group = self.request.query_params.get('group', None)
        if group is not None:
            return self.queryset.filter(group=group)
        try:
            followigs = Profile.get_followin(
                self.request)

            return self.queryset.filter(Q(created_by_id__in=followigs.values_list(
                'followin', flat=True)) | Q(created_by_id=self.request.user.id))
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

    def postsOfuser(self, request, pk=None):

        queryset = Post.objects.filter(
            created_by=pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def weeklyLikeRanking(self, request):
        like = self.request.query_params.get('like', None)
        today = timezone.now()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        print(like)
        if(like == True or like == 'true'):
            print("like")
            queryset = Post.objects.filter(
                Q(created_at__range=(start, end))).annotate(num_likes=Count('postlike__liked_by', distinct=True)).order_by('-num_likes')[:1]
        else:
            print("dislike")

            queryset = Post.objects.filter(
                Q(created_at__range=(start, end))).annotate(num_deslikes=Count('postlike__disliked_by', distinct=True)).order_by('-num_deslikes')[:1]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
