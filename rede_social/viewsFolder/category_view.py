

from rede_auth.permissions import IsTeacher
from rede_auth.views.mixed_view import MixedPermissionModelViewSet
from rede_social.models import Category
from rede_social.serializers.category_serializer import CategorySerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser


class CategoryViewSet(MixedPermissionModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes_by_action = {
        'create': [IsAuthenticated],
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

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
