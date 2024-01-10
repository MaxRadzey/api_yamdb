from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404

import random
import string

from reviews.models import Title, Review


def calculate_rating(data):
    """Функция для вычисления рейтинга произведения"""
    return None


def send_confirmation_email(user):
    """Функция для отправки письма с кодом подтверждения"""
    confirmation_code = ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=6
        )
    )
    user.confirmation_code = confirmation_code
    user.save()

    send_mail(
        'Your confirmation code',
        f'Your confirmation code is {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


def get_title(data):
    title_id = data.get('title_id')
    return get_object_or_404(Title, pk=title_id)


def get_review(data):
    review_id = data.get('review_id')
    return get_object_or_404(Review, pk=review_id)
