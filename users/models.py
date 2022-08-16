from django.db import models

from core.models import TimeStampModel


class User(TimeStampModel):
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=300)
    password = models.CharField(max_length=200)

    class Meta():
        db_table = 'users'