import json
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
from rede_social.serializers.post_serializer import PostSerializer
from rede_social.serializers.profile_serializer import ProfileGetSerializer, ProfileSerializer
from rede_social.models import Category, Following, Post, Profile


def follow(request, user_to_follow):
    main_user = request.user
    to_follow = User.objects.get(email=user_to_follow.email)
    main_user_followers = Following.objects.filter(user=main_user, followed=to_follow)
    is_following = True if main_user_followers else False
    if is_following:
        Following.unfollow(main_user, to_follow)
        is_following = False
    else:
        Following.follow(main_user, to_follow)
        is_following = True

    context = {
        "following?":is_following
    }
    response = json.dumps(context)

    return HttpResponse(response, content_type='aplication/json')

class PostViewSet(MixedPermissionModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [IsAuthenticated],
        'delete': [IsSameUser],
        'update': [IsSameUser],
        'partial_update':[IsSameUser]
    }
    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        try:
            id = self.request.query_params.get('id', None)
            if id is not None:
                user = User.objects.get(id = id)
                return self.queryset.filter(user=user)
        except TypeError as e:
            pass
        return self.queryset 

class CategoryViewSet(MixedPermissionModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes_by_action = {
        'create': [IsTeacher],
        'list': [IsAuthenticated],
        'delete': [IsTeacher],
        'update': [IsTeacher],
        'partial_update':[IsTeacher]
    }
    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        try:
            id = self.request.query_params.get('id', None)
            if id is not None:
                user = User.objects.get(id = id)
                return self.queryset.filter(user=user)
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
                user = User.objects.get(id = id)
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


