
from rede_auth.models import User
from rede_auth.permissions import IsSameUser
from rede_auth.views.mixed_view import MixedPermissionModelViewSet
from rede_social.models import Forms

from rede_social.pagination.LargeResultsSetPagination import StandardResultsSetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from ..serializers.forms_serializer import FormsSerializer


class FormsViewSet(MixedPermissionModelViewSet):
    queryset = Forms.objects.all()
    serializer_class = FormsSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes_by_action = {
        'create': [AllowAny],
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
                return self.queryset.filter(pk=id)
        except TypeError as e:
            pass
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_serializer_class(self):
        # delete_users_and_channels()
        if self.request.method == "GET":
            return FormsSerializer

        elif self.request.method in ['PUT', 'PATCH', 'POST']:
            return FormsSerializer
        else:
            return FormsSerializer
