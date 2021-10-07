"""rede URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#models
from rede_auth.views.user_views import StudentViewSet, TeacherViewSet

#django
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve 

#rest
from rest_framework import routers, serializers, viewsets
from rest_framework_simplejwt import views as jwt_views

from . import settings
from rede_auth.views.webtoken_views import *


router = routers.DefaultRouter()
router.register(r'Aluno', StudentViewSet)
router.register(r'Profesor', TeacherViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', MyObtainJSONWebToken.as_view(), name='login_jwt'),
    #path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    #path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]

urlpatterns += staticfiles_urlpatterns()
