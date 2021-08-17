from rede_auth.models import User
from rede_auth.views.mixed_view import MixedPermissionModelViewSet
from rede_auth.serializers.user_serializer  import UserSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated)

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)

    # def create(self, request, *args, **kwarsg):
    #     return Response({"error": "Method POST not allowed."}, 405)