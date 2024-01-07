from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from http import HTTPStatus
from rest_framework import views, generics, filters, viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.utils import send_confirmation_email
from .serializers import (
    CreateUserSerializer,
    SignUpSerializer,
    TokenSerializer,
    CurrentUserSerializer
)
from api.permissions import IsAdmin

User = get_user_model()


class UserView(viewsets.ModelViewSet):
    """Создание и редактирование пользователя администратором."""
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [IsAdmin,]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'head', 'delete', 'patch']

    def get_object(self):
        """Override to allow retrieval of users by username instead of ID."""
        username = self.kwargs.get('pk')  # 'pk' is the default name for detail route parameter
        return get_object_or_404(User, username=username)


class CurrentUserView(generics.RetrieveUpdateAPIView):
    """
    A view that allows the action 'GET' and 'PATCH' to be performed
    on the authenticated user.
    """
    serializer_class = CurrentUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def get_object(self):
        if not self.request.user.is_authenticated:
            raise AuthenticationFailed("Вы не авторизованы.")
        return get_object_or_404(
            User,
            username=self.request.user.username
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
