from http import HTTPStatus

from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import views, filters, viewsets, status
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
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticatedOrReadOnly,]
    )
    def me(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Вы не авторизованы."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if request.method.lower() == 'get':
            serializer = CurrentUserSerializer(request.user)
            return Response(serializer.data)
        elif request.method.lower() == 'patch':
            serializer = CurrentUserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class SignUpView(views.APIView):
    """Самостоятельная регистрация нового пользователя."""
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user, _ = User.objects.get_or_create(**serializer.validated_data)
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
    permission_classes = [AllowAny, ]

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
