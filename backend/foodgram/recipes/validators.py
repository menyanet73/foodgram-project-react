import re

from django.core.exceptions import ValidationError


def validate_color(value):
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value)
    if not len(value) == 7 or not match:
        raise ValidationError('Wrong color type, must be #ffffff hex type.')
