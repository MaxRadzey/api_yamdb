from django.contrib.auth import get_user_model
from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.utils import send_confirmation_email
from .serializers import (
    DBUserTokenObtainPairSerializer,
    RegisterSerializer
)

User = get_user_model()


class SignUpView(views.APIView):
    serializer_class = DBUserTokenObtainPairSerializer
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.validated_data)
        send_confirmation_email(user)
        return Response(
            {'detail': 'Confirmation code sent to your email'},
            status=status.HTTP_200_OK
        )


class TokenView(views.APIView):
    serializer_class = RegisterSerializer,
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(
            **serializer.validated_data
        ).first()
        if not user:
            return Response(
                {'detail': 'Invalid username or confirmation code'},
                status=status.HTTP_400_BAD_REQUEST
            )
        refresh = RefreshToken.for_user(user)
        return Response(
            {'token': str(refresh.access_token)},
            status=status.HTTP_200_OK
        )
