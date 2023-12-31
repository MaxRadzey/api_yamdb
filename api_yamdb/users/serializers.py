from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'role', 'password')
        extra_kwargs = {
            'username': {'required': True},
            'email': {
                'required': True,
                'validators': [UniqueValidator(queryset=User.objects.all())]
            },
            'role': {'required': False},
            'password': {'write_only': True, 'required': False},
        }


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
