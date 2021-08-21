from rede_auth.models import Student, User
from rest_framework import serializers, routers
from rest_framework import routers, serializers, viewsets
from rede_auth.helpers import validate_cpf
from django.contrib.auth import password_validation

class UserSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        max_length=100, write_only=True, required=False)
        
    class Meta:
        model=User
        fields = [
            'id',
            'nome',
            'user_type',
            'email',
            'password',
            'password_confirmation',
            'old_password',
            'phonenumber',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirmation': {'write_only': True},
        }

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = [
            'id',
            'nome',
            'email',
            'password',
            'password_confirmation',
            'birthdate',
            'phonenumber',
            'picture',
            'user_type',
            'cpf',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirmation': {'write_only': True},
            'user_type': {'read_only': True}
        }

    def validate_password(self, value):
        try:
            password_validation.validate_password(value, self.instance)
        except serializers.ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value
    
    def validate(self, data):
        # add here additional check for password strength if needed
        if data.get('password_confirmation') != data.get('password'):
            raise serializers.ValidationError(
                {'password': 'A senha precisa ser confirmada corretamente'})

        return data
    def create(self, validated_data):
        validated_data['username'] = validated_data['email'].split('@')[0]
        user = Student.objects.create_user(**validated_data)
        user.password_confirmation = ''
        user.user_type = "Aluno"
        user.save()
        print("######################### Criando Aluno: ", user)

        return user

    def update(self, instance, validated_data):
        for key in validated_data.keys():
            if 'password' != key:
                instance.__setattr__(key, validated_data[key])
            else:
                instance.set_password(validated_data[key])
        instance.password_confirmation = ''
        instance.save()
        return instance   


class StudentGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = [
            'id',
            'nome',
            'email',
            'birthdate',
            'phonenumber',
            'picture',
            'cpf',
            'user_type',
            'customer_address',
        ]
