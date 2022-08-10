from rede_auth.models import Student, User, Teacher
from rede_auth.views.mixed_view import MixedPermissionModelViewSet
from rede_auth.serializers.user_serializer import TeacherSerializer, UserSerializer, UserGetSerializer, StudentSerializer, StudentGetSerializer, TeacherGetSerializer
from rede_auth.permissions import *

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import filters

from rede_social.pagination.LargeResultsSetPagination import StandardResultsSetPagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = UserSerializer
    search_fields = ['nome', 'email']
    filter_backends = [filters.SearchFilter]
    permission_classes_by_action = {'create': [AllowAny],
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
                return self.queryset.filter(id=int(id))
        except TypeError as e:
            pass
        return self.queryset

    def get_serializer_class(self):
        # delete_users_and_channels()
        if self.request.method == "GET":
            return UserGetSerializer
        elif self.request.method in ['PUT', 'PATCH', 'POST']:
            return UserSerializer
        else:
            return UserGetSerializer


class StudentViewSet(MixedPermissionModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    permission_classes_by_action = {'create': [AllowAny],
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
                return self.queryset.filter(id=int(id))
        except TypeError as e:
            pass
        return self.queryset

    def get_serializer_class(self):
        # delete_users_and_channels()
        if self.request.method == "GET":
            return StudentGetSerializer
        elif self.request.method in ['PUT', 'PATCH', 'POST']:
            return StudentSerializer
        else:
            return StudentGetSerializer


class TeacherViewSet(MixedPermissionModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    permission_classes_by_action = {'create': [AllowAny],
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
                return self.queryset.filter(id=int(id))
        except TypeError as e:
            pass
        return self.queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TeacherGetSerializer
        elif self.request.method in ['PUT', 'PATCH', 'POST']:
            return TeacherSerializer
        else:
            return TeacherGetSerializer
