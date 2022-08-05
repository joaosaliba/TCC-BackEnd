
from rede_auth.models import User
from rede_auth.permissions import IsSameUser
from rede_auth.views.mixed_view import MixedPermissionModelViewSet
from rede_social.models import Following

from rede_social.pagination.LargeResultsSetPagination import StandardResultsSetPagination
from rede_social.serializers.comments_serializer import CommentsSerializer, CommentsGetSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from rede_social.serializers.follow_serializer import FollowingSerializer


class FollowViewSet(MixedPermissionModelViewSet):
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [IsAuthenticated],
        'delete': [IsSameUser],
        'update': [IsSameUser],
        'partial_update': [IsSameUser]
    }

    def create(self, serializer):
        main_user = self.request.user
        to_follow = User.objects.get(pk=self.request.data['follow'])
        main_user_followers = Following.objects.filter(
            user=main_user, follow=to_follow)
        is_following = True if main_user_followers else False
        queryset = Following.objects.filter(
            user=main_user)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        if is_following:
            Following.unfollow(main_user, to_follow)
            return self.get_paginated_response(serializer.data)
        else:
            Following.follow(main_user, to_follow)
            return self.get_paginated_response(serializer.data)
