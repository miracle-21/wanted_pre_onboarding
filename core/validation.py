import re

from django.core.exceptions import ValidationError

#PASSWORD_REGEX: 4자 이상
PASSWORD_REGEX = '.{4,}$'

def validate_password(value):
    if not re.match(PASSWORD_REGEX,value):
        raise ValidationError('Invalid Password')