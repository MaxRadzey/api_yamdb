from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import filters, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsAdmin
from api.utils import send_confirmation_email
from users.serializers import (CreateUserSerializer, CurrentUserSerializer,
                               SignUpSerializer, TokenSerializer)

User = get_user_model()


class UserView(viewsets.ModelViewSet):
    """Создание и редактирование пользователя администратором."""

    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'head', 'delete', 'patch']
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        """Получение и редактирование данных текущего пользователя."""
        if request.method.lower() == 'get':
            serializer = CurrentUserSerializer(request.user)
            return Response(serializer.data)
        else:
            serializer = CurrentUserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)


class SignUpView(views.APIView):
    """Самостоятельная регистрация нового пользователя."""

    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user, _ = User.objects.get_or_create(**serializer.validated_data)
            send_confirmation_email(user)
            return Response(
                {
                    'username': user.username,
                    'email': user.email,
                },
                status=HTTPStatus.OK
            )


class TokenView(views.APIView):

    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                {'detail': 'Неверный код подтверждения'},
                status=HTTPStatus.BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {'token': str(refresh.access_token)},
            status=HTTPStatus.OK
        )
