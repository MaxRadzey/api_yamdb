from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    """Валидация поля года."""
    if value > datetime.now().year:
        raise ValidationError(
            ('Нельзя указывать год в будущем!')
        )
