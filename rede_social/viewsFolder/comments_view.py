
from rede_auth.permissions import IsSameUser
from rede_auth.views.mixed_view import MixedPermissionModelViewSet

from rede_social.models import Comments
from rede_social.serializers.comments_serializer import CommentsSerializer, CommentsGetSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser


from rest_framework.decorators import action
from django.http import JsonResponse


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
