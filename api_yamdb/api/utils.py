from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from reviews.models import Review, Title


def calculate_rating(data):
    """Функция для вычисления рейтинга произведения"""
    return None


def send_confirmation_email(user):
    """Функция для отправки письма с кодом подтверждения"""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    send_mail(
        'Your confirmation code',
        f'Your confirmation code is {token}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    return uid, token


def get_title(data):
    title_id = data.get('title_id')
    return get_object_or_404(Title, pk=title_id)


def get_review(data):
    review_id = data.get('review_id')
    return get_object_or_404(Review, pk=review_id)
