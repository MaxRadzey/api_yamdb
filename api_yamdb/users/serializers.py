from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.constants import EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH
from users.validators import validate_username

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            MaxLengthValidator(EMAIL_MAX_LENGTH),
        ]
    )
    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            MaxLengthValidator(USERNAME_MAX_LENGTH),
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Invalid email format.'
            ),
            validate_username
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
            MaxLengthValidator(USERNAME_MAX_LENGTH),
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Неверный формат адреса.'
            ),
            validate_username
        ]
    )
    email = serializers.EmailField(
        required=True,
        validators=[
            MaxLengthValidator(EMAIL_MAX_LENGTH)
        ]
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        user_with_same_email = User.objects.filter(email=email).first()
        user_with_same_username = User.objects.filter(
            username=username
        ).first()

        if user_with_same_email and user_with_same_email.username != username:
            raise serializers.ValidationError(
                "Такой email уже зарегистрирован."
            )

        if user_with_same_username and user_with_same_username.email != email:
            raise serializers.ValidationError(
                "Такой username уже зарегистрирован."
            )
        return data


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
