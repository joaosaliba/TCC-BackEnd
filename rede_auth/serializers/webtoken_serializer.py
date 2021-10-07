#rest
from rest_framework_jwt.serializers import *
from rest_framework import routers, serializers

#django
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext as _
from django.template.loader import get_template

#models
from rede_auth.models import *

#serializers
from rede_auth.serializers.user_serializer import *


def jwt_response_payload_handler(token, user=None, request=None, player_id=None):
    print({'request': request.data})
    return {
        'token': token,
        'player_id': player_id,
        'user': UserSerializer(user, context={'request': request}).data
    }


class MyJSONWebTokenSerializer(JSONWebTokenSerializer):
    """
    Serializer class used to validate a username and password.

    'username' is identified by the custom UserModel.USERNAME_FIELD.

    Returns a JSON Web Token that can be used to authenticate later calls.
    """
    device_type = serializers.ChoiceField(write_only=True,choices=(('ANDROID', 'ANDROID'),('APPLE', 'APPLE')))
    device_id = serializers.CharField(write_only=True, allow_null=True, required=False)

    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super(JSONWebTokenSerializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField(write_only=True)

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password'),
            'device_type': attrs.get('device_type')
        }
        print("############################# credenciais", credentials['email'])
        if all(credentials.values()):
            if 'device_id' in attrs.keys():
                did = attrs.pop('device_id')
            else:
                did = None
            dtype = credentials.pop('device_type')
            try:
                user = authenticate(**credentials)
                print("############################# credenciais", credentials)
            except Exception as e:
                print(e)
            print("####################### user : ", user)
            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError({"email": msg})
                
                payload = jwt_payload_handler(user)
                print("payload foi")
                token = jwt_encode_handler(payload)
                print("token foi")

                # if not player_id:
                #     raise serializers.ValidationError({"device_id": _("Player Id not created")})

                return {
                    'token': token,
                    'user': user,
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError({"email": msg})
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError({"error": msg})