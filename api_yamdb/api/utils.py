from django.core.mail import send_mail
from django.conf import settings
import random
import string


def calculate_rating(data):
    """Функция для вычисления рейтинга произведения"""
    return None


def send_confirmation_email(user):
    """Функция для отправки письма с кодом подтверждения"""
    confirmation_code = ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=20
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
