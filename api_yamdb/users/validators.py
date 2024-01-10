from rest_framework.validators import ValidationError


def validate_username(value):
    """Валидация username.
    Запрещено использовать username 'me'.
    """
    if value.lower() == 'me':
        raise ValidationError("Такой username недопустим.")
    return value
