from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, RegexValidator
from rest_framework.validators import UniqueValidator, ValidationError

User = get_user_model()


def validate_username(value):
    """Валидация username.
    Запрещено использовать username 'me'.
    """
    if value.lower() == 'me':
        raise ValidationError("Такой username недопустим.")
    return value


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            MaxLengthValidator(254),
        ]
    )
    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            MaxLengthValidator(150),
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Invalid email format.'
            ),
            validate_username
        ]
    )
    first_name = serializers.CharField(
        required=False,
        validators=[
            MaxLengthValidator(150)
        ]
    )
    last_name = serializers.CharField(
        required=False,
        validators=[
            MaxLengthValidator(150)
        ]
    )

    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'role', 'bio'
        )


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[
            MaxLengthValidator(150),
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Invalid email format.'
            ),
            validate_username
        ]
    )
    email = serializers.EmailField(
        required=True,
        validators=[
            MaxLengthValidator(254)
        ]
    )

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username',
            'bio', 'email', 'role'
        )
        read_only_fields = ('role',)
