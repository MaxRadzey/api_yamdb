from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from models import DBUser


class DBUserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=DBUser.objects.all())]
    )

    class Meta:
        model = DBUser
        fields = ('username', 'email',)
        extra_kwargs = {
            'username': {'required': True},
        }

    def create(self, validated_data):
        user = DBUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.save()

        return user

# TODO сделать сериализаторы для профиля и для изменения профиля
