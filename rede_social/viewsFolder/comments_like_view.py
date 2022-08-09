

from django.shortcuts import get_object_or_404
from rede_auth.permissions import IsSameUser
from rede_auth.views.mixed_view import MixedPermissionModelViewSet
from rede_social.models import CommentLike, Comments, Post, PostLike
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rede_social.permissions import hasSelfVotedOrReadOnly
from rede_social.serializers.comment_like_serializer import CommentLikeSerializer


class CommentLikeViewSet(MixedPermissionModelViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [IsAuthenticated],
        'delete': [IsSameUser],
        'update': [IsSameUser],
        'partial_update': [IsSameUser]
    }

    def perform_create(self, serializer):
        comment_instance = get_object_or_404(
            Comments, pk=self.request.data['liked_comment'])

        # if user likes the post
        if self.request.data['like']:
            already_up_voted = CommentLike.objects.filter(
                liked_comment=comment_instance, comment_liked_by=self.request.user).exists()
            if already_up_voted:
                CommentLike.objects.filter(
                    liked_comment=comment_instance, comment_liked_by=self.request.user).delete()
            else:
                already_down_voted = CommentLike.objects.filter(
                    liked_comment=comment_instance, comment_disliked_by=self.request.user).exists()
                if already_down_voted:
                    CommentLike.objects.filter(
                        liked_comment=comment_instance, comment_disliked_by=self.request.user).delete()
                serializer.save(comment_liked_by=self.request.user,
                                liked_comment=comment_instance)
        # if dislikes
        else:
            already_down_voted = CommentLike.objects.filter(
                liked_comment=comment_instance, comment_disliked_by=self.request.user).exists()
            if already_down_voted:
                CommentLike.objects.filter(
                    liked_comment=comment_instance, comment_disliked_by=self.request.user).delete()
            else:
                already_up_voted = CommentLike.objects.filter(
                    liked_comment=comment_instance, comment_liked_by=self.request.user).exists()
                if already_up_voted:
                    CommentLike.objects.filter(
                        liked_comment=comment_instance, comment_liked_by=self.request.user).delete()
                serializer.save(comment_disliked_by=self.request.user,
                                liked_comment=comment_instance)
