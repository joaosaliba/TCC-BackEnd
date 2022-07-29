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
# models
from rede_auth.views.user_views import StudentViewSet, TeacherViewSet, UserViewSet

# django
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from django.conf.urls.static import static
from rede_social.viewsFolder.announcements_view import AnnouncementViewSet
from rede_social.viewsFolder.category_view import CategoryViewSet
from rede_social.viewsFolder.comments_like_view import CommentLikeViewSet
from rede_social.viewsFolder.comments_view import CommentsViewSet
from rede_social.viewsFolder.post_like_view import PostLikeViewSet
from rede_social.viewsFolder.post_view import PostViewSet
from rede_social.viewsFolder.profile_view import ProfileViewSet

# rest
from rest_framework import routers, serializers, viewsets
from rest_framework_simplejwt import views as jwt_views


from django.conf import settings
from rede_auth.views.webtoken_views import *
from emailer import urls as URLmailer

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
# router.register(r'aluno', StudentViewSet)
# router.register(r'professor', TeacherViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'post', PostViewSet)
router.register(r'announcement', AnnouncementViewSet)
router.register(r'comments', CommentsViewSet)
router.register(r'likePost', PostLikeViewSet)
router.register(r'likeComment', CommentLikeViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('mailer', include(URLmailer)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', MyObtainJSONWebToken.as_view(), name='login_jwt'),
    path('logout_token/', APILogoutView.as_view(), name='logout_token'),
    path(r'api/password_reset/',
         include('django_rest_passwordreset.urls', namespace='password_reset')),

    # path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    # path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

    path('comments/postComments/<int:pk>/',
         CommentsViewSet.as_view({'get': 'commetsOfPosts'}), name='postComments'),

    path('post/user/<int:pk>/',
         PostViewSet.as_view({'get': 'postsOfuser'}), name='postsOfuser'),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
