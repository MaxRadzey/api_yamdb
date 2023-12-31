from django.contrib.auth import get_user_model
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.utils import send_confirmation_email

User = get_user_model()


class SignUpView(views.APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        username = request.data.get('username')
        if not email or not username:
            return Response(
                {'detail': 'Email and username are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.create_user(username=username, email=email)
        send_confirmation_email(user)
        return Response(
            {'detail': 'Confirmation code sent to your email'},
            status=status.HTTP_200_OK
        )


class TokenView(views.APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        user = User.objects.filter(
            username=username,
            confirmation_code=confirmation_code
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
