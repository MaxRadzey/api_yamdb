from django.urls import path
from .views import SignUpView, TokenView

urlpatterns = [
    path(
        'signup/',
        SignUpView.as_view(),
        name='signup'
    ),
    path(
        'token/',
        TokenView.as_view(),
        name='token'
    ),
]
