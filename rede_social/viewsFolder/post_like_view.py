

from django.shortcuts import get_object_or_404
from rede_auth.permissions import IsSameUser
from rede_auth.views.mixed_view import MixedPermissionModelViewSet
from rede_social.serializers.like_post_serializer import PostLikeSerializer
from rede_social.models import Post, PostLike
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rede_social.permissions import hasSelfVotedOrReadOnly


class PostLikeViewSet(MixedPermissionModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [IsAuthenticated],
        'delete': [IsSameUser],
        'update': [IsSameUser],
        'partial_update': [IsSameUser]
    }

    def perform_create(self, serializer):
        post_instance = get_object_or_404(
            Post, pk=self.request.data['liked_post'])

        # if user likes the post
        if self.request.data['like']:
            already_up_voted = PostLike.objects.filter(
                liked_post=post_instance, liked_by=self.request.user).exists()
            if already_up_voted:
                PostLike.objects.filter(
                    liked_post=post_instance, liked_by=self.request.user).delete()
            else:
                already_down_voted = PostLike.objects.filter(
                    liked_post=post_instance, disliked_by=self.request.user).exists()
                if already_down_voted:
                    PostLike.objects.filter(
                        liked_post=post_instance, disliked_by=self.request.user).delete()
                serializer.save(liked_by=self.request.user,
                                liked_post=post_instance)
        # if dislikes
        else:
            already_down_voted = PostLike.objects.filter(
                liked_post=post_instance, disliked_by=self.request.user).exists()
            if already_down_voted:
                PostLike.objects.filter(
                    liked_post=post_instance, disliked_by=self.request.user).delete()
            else:
                already_up_voted = PostLike.objects.filter(
                    liked_post=post_instance, liked_by=self.request.user).exists()
                if already_up_voted:
                    PostLike.objects.filter(
                        liked_post=post_instance, liked_by=self.request.user).delete()
                serializer.save(disliked_by=self.request.user,
                                liked_post=post_instance)
