from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from http import HTTPStatus
from rest_framework import views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.utils import send_confirmation_email
from .serializers import (
    CreateUserSerializer,
    SignUpSerializer,
    TokenSerializer,
)
from api.permissions import IsAdmin

User = get_user_model()


class CreateUserView(views.APIView):
    """Создание пользователя администратором."""
    serializer_class = CreateUserSerializer
    permission_classes = [IsAdmin,]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.validated_data)
        return Response(
            {
                'username': user.username,
                'email': user.email},
            status=HTTPStatus.CREATED
        )


class SignUpView(views.APIView):
    """Самостоятельная регистрация нового пользователя."""
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                if user.username != username:
                    return Response(
                        {'detail': 'Такой email уже зарегистрирован'},
                        status=HTTPStatus.BAD_REQUEST
                    )
                send_confirmation_email(user)
                return Response(
                    {
                        'username': user.username,
                        'email': user.email
                    },
                    status=HTTPStatus.OK
                )
            elif User.objects.filter(username=username).exists():
                return Response(
                    {'detail': 'Такой username уже зарегистрирован'},
                    status=HTTPStatus.BAD_REQUEST
                )
            else:
                user = User.objects.create(
                    username=username,
                    email=email
                )
                send_confirmation_email(user)
                return Response(
                    {
                        'username': user.username,
                        'email': user.email
                    },
                    status=HTTPStatus.OK
                )
        else:
            return Response(
                serializer.errors,
                status=HTTPStatus.BAD_REQUEST
            )


class TokenView(views.APIView):
    serializer_class = TokenSerializer
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)

        if user.confirmation_code != confirmation_code:
            return Response(
                {'detail': 'Неверный код подтверждения'},
                status=HTTPStatus.BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {'token': str(refresh.access_token)},
            status=HTTPStatus.OK
        )
