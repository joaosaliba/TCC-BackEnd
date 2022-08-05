
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.dispatch import receiver
from emailer.views import send
from django_rest_passwordreset.signals import reset_password_token_created
from django.urls import reverse
import datetime
# views
from rede_auth.serializers.webtoken_serializer import jwt_response_payload_handler

# settings
from django.conf import settings
# serializers
from rede_auth.serializers.webtoken_serializer import MyJSONWebTokenSerializer

# django
from django.conf import settings

# Django rest
from rest_framework_jwt.settings import api_settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework import views, status, viewsets
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.response import Response
from rest_framework.permissions import *

from rest_condition import Or


class MyObtainJSONWebToken(ObtainJSONWebToken):
    serializer_class = MyJSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            player_id = serializer.object.get('player_id')

            response_data = jwt_response_payload_handler(
                token, user, request, player_id)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APILogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})

        return Response({"status": "OK, goodbye"})


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(
        ('http://redefelicidade.duckdns.org/newPassword'), reset_password_token.key)

    send(
        # title:
        "Password Reset para {title}".format(title="Rede Felicidade"),
        # message:
        email_plaintext_message,
        # to:
        [reset_password_token.user.email]
    )
