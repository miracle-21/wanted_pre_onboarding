from django.db import models
from companies.models import Announcement

from core.models import TimeStampModel


class User(TimeStampModel):
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=300)
    password = models.CharField(max_length=200)

    class Meta():
        db_table = 'users'

class Apply(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta():
        db_table = 'apply'