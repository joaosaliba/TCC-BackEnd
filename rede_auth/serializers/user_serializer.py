import profile
from rede_social.serializers.profile_serializer import ProfileGetSerializer, ProfileSerializer
from attr import fields
from rede_auth.models import Student, Teacher, User
from rede_social.models import Profile
from rest_framework import serializers, routers
from rest_framework import routers, serializers, viewsets
from rede_auth.helpers import validate_cpf
from django.contrib.auth import password_validation
from django.db.models import ImageField

from rede_social.serializers.profile_serializer import ProfileUserSerializer


class UserSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        max_length=100, write_only=True, required=False)
    picture = serializers.ImageField(allow_empty_file=True, required=False)
    password_confirmation = serializers.CharField(required=False)
    profile = ProfileUserSerializer()

    class Meta:
        model = User
        fields = [
            'id',
            'nome',
            'email',
            'password',
            'password_confirmation',
            'profile',
            'phonenumber',
            'picture',
            'user_type',
            'old_password',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirmation': {'write_only': True, 'required': False},
            'old_password': {'write_only': True, 'required': False},
            'user_type': {'required': True},
            'picture': {'required': False},
            'profile': {'required': False},
            'cpf': {'required': False},
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
        userType = validated_data['user_type']
        profile_data = validated_data.pop('profile')

        if(userType == "Professor"):
            user = Teacher.objects.create_user(**validated_data)
        if(userType == "Aluno"):
            user = Student.objects.create_user(**validated_data)

        profile = Profile.objects.create(user=user)
        for field in profile_data:
            profile.__setattr__(field, profile_data.get(field))
        profile.save()
        print("######################### Criando Profile: ", profile)

        user.password_confirmation = ''
        user.user_type = validated_data['user_type']
        user.save()
        print("######################### Criando Usuario: ", user)

        return user

    def update(self, instance, validated_data):
        profile = Profile.objects.get(user=instance)
        profile_data = validated_data.pop('profile')
        for field in profile_data:
            profile.__setattr__(field, profile_data.get(field))
        profile.save()
        for field in validated_data:
            if field == 'password':
                instance.set_password(validated_data.get(field))
            else:
                instance.__setattr__(field, validated_data.get(field))

        instance.save()
        return instance


class UserGetSerializer(serializers.ModelSerializer):
    profile = ProfileGetSerializer()

    class Meta:
        model = User
        fields = [
            'id',
            'nome',
            'email',
            'phonenumber',
            'picture',
            'user_type',
            'profile',
            'created_at'
        ]
        extra_kwargs = {
            'user_type': {'read_only': True},
            'picture': {'required': False},
            'profile': {'required': False},
        }


class StudentSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(allow_empty_file=True, required=False)
    password_confirmation = serializers.CharField(required=False)

    class Meta:
        model = Student
        fields = [
            'id',
            'nome',
            'email',
            'password',
            'password_confirmation',
            'profile',
            'phonenumber',
            'picture',
            'user_type',
            'cpf',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirmation': {'write_only': True, 'required': False},
            'user_type': {'read_only': True},
            'picture': {'required': False},
            'profile': {'required': False},
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
        profile_data = validated_data.pop('profile')
        profile = Profile.objects.create(
            user=user)
        profile.birthdate = profile_data['birthdate']
        profile.save()
        print("######################### Criando Profile: ", profile)
        user.password_confirmation = ''
        user.user_type = "Aluno"
        user.save()
        print("######################### Criando Aluno: ", user)

        return user

    def update(self, instance, validated_data):
        for field in validated_data:
            if field == 'password':
                instance.set_password(validated_data.get(field))
            else:
                instance.__setattr__(field, validated_data.get(field))
            instance.save()
        return instance


class StudentGetSerializer(serializers.ModelSerializer):
    profile = ProfileGetSerializer()

    class Meta:
        model = Student
        fields = [
            'id',
            'nome',
            'email',
            'phonenumber',
            'picture',
            'user_type',
            'cpf',
            'profile'
        ]


class TeacherSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(allow_empty_file=True, required=False)
    password_confirmation = serializers.CharField(required=False)

    class Meta:
        model = Teacher
        fields = [
            'id',
            'nome',
            'email',
            'password',
            'password_confirmation',
            'phonenumber',
            'picture',
            'user_type',
            'cpf',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirmation': {'write_only': True, 'required': False},
            'user_type': {'read_only': True},
            'picture': {'required': False}

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
        user = Teacher.objects.create_user(**validated_data)
        profile = Profile.objects.create(user=user)
        profile.save()
        print("######################### Criando Profile: ", profile)
        user.password_confirmation = ''
        user.user_type = "Professor"
        user.save()
        print("######################### Criando Professor: ", user)

        return user

    def update(self, instance, validated_data):
        for field in validated_data:
            if field == 'password':
                instance.set_password(validated_data.get(field))
            else:
                instance.__setattr__(field, validated_data.get(field))
            instance.save()
        return instance


class TeacherGetSerializer(serializers.ModelSerializer):
    profile = ProfileGetSerializer()

    class Meta:
        model = Teacher
        fields = [
            'id',
            'nome',
            'email',
            'phonenumber',
            'picture',
            'user_type',
            'cpf',
            'profile'
        ]
