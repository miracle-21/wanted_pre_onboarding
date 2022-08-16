import re

from django.core.exceptions import ValidationError

#PASSWORD_REGEX: 4자 이상
PASSWORD_REGEX = '.{4,}$'
#EMAIL_REGEX: @와 .필수
EMAIL_REGEX    = '^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$'

def validate_password(value):
    if not re.match(PASSWORD_REGEX,value):
        raise ValidationError('Invalid Password')

def validate_email(value):
    if not re.match(EMAIL_REGEX,value):
        raise ValidationError('Invalid Email')