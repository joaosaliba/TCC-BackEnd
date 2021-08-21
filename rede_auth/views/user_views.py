from rede_auth.models import Student, User, Teacher
from rede_auth.views.mixed_view import MixedPermissionModelViewSet
from rede_auth.serializers.user_serializer  import  TeacherSerializer, UserSerializer, StudentSerializer
from rede_auth.permissions import *
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


class StudentViewSet(MixedPermissionModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    permission_classes_by_action = {'create': [AllowAny],
                                    'list': [AllowAny],
                                    'delete': [IsSameUser],
                                    'update': [IsSameUser],
                                    'partial_update': [IsSameUser]
                                    }

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        return Student.objects.filter(id=self.request.user.id)

class TeacherViewSet(MixedPermissionModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    permission_classes_by_action = {'create': [AllowAny],
                                    'list': [AllowAny],
                                    'delete': [IsSameUser],
                                    'update': [IsSameUser],
                                    'partial_update': [IsSameUser]
                                    }

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        return Student.objects.filter(id=self.request.user.id)
