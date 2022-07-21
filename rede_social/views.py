import json

from django.http import HttpResponse
from rede_auth.views.mixed_view import MixedPermissionModelViewSet
from rede_auth.models import User
from rede_social.serializers.like_post_serializer import PostLikeSerializer
from rede_social.models import Following, PostLike


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


class PostLikeViewSet(MixedPermissionModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
