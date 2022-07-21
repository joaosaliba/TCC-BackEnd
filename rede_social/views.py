import json
from unicodedata import category
from django.db.models import query
from django.shortcuts import render
from django.http import HttpResponse

from rede_auth.views.mixed_view import MixedPermissionModelViewSet
from rede_auth.permissions import IsSameUser, IsTeacher
from rede_auth.models import User

from rest_framework.serializers import Serializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from rede_social.serializers.category_serializer import CategorySerializer
from rede_social.serializers.post_serializer import PostSerializer, PostGetSerializer
from rede_social.serializers.comments_serializer import CommentsSerializer, CommentsGetSerializer
from rede_social.serializers.like_post_serializer import PostLikeSerializer

from rede_social.serializers.profile_serializer import ProfileGetSerializer, ProfileSerializer
from rede_social.serializers.announcement_serializer import AnnouncementSerializer
from rede_social.models import Announcement, Category, Following, Post, Profile, Comments, PostLike

from rest_framework.decorators import action
from django.http import JsonResponse


def follow(request, user_to_follow):
    main_user = request.user
    to_follow = User.objects.get(email=user_to_follow.email)
    main_user_followers = Following.objects.filter(
        user=main_user, followed=to_follow)
    is_following = True if main_user_followers else False
    if is_following:
        Following.unfollow(main_user, to_follow)
        is_following = False
    else:
        Following.follow(main_user, to_follow)
        is_following = True

    context = {
        "following?": is_following
    }
    response = json.dumps(context)

    return HttpResponse(response, content_type='aplication/json')


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


class CategoryViewSet(MixedPermissionModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes_by_action = {
        'create': [AllowAny],
        'list': [IsAuthenticated],
        'delete': [IsTeacher],
        'update': [IsTeacher],
        'partial_update': [IsTeacher]
    }

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        try:
            pk = self.request.query_params.get('pk', None)
            if pk is not None:
                category = Category.objects.get(pk=pk)
                return self.queryset.filter(category=category)
        except TypeError as e:
            pass
        return self.queryset


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


class CommentsViewSet(MixedPermissionModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [IsAuthenticated],
        'delete': [IsSameUser],
        'update': [IsSameUser],
        'partial_update': [IsSameUser]
    }

    @action(detail=False, methods=['GET'], name='Get comments from Post')
    def postComments(request, postId):
        queryset = Comments.objects.filter(
            post_id=postId)

        serializer = CommentsGetSerializer(queryset, many=True)

        return JsonResponse(serializer.data, safe=False)

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

    def perform_create(self, serializer):
        serializer.save(commented_by=self.request.user)


class PostLikeViewSet(MixedPermissionModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
