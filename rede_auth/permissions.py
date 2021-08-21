from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
from rest_framework.exceptions import PermissionDenied
from rede_auth.models import *
import logging

class WriteOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST'

class IsSameUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True            

        return request.user.id == obj.id


class WithoutPermissions(BasePermission):
    def has_permission(self, request, view):
       return False

    def has_object_permission(self, request, view, obj):       
        return False


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True 
        return request.user.is_authenticated and request.user.user_type == "Professor"

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.user_type == "Professor":
            return True

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True 
        return request.user.is_authenticated and request.user.user_type == "Aluno"

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.user_type == "Aluno":
            return True
        return False


    