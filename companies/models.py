from django.db import models
from core.models import TimeStampModel

class Company(models.Model):
    name = models.CharField(max_length = 100)
    nation = models.CharField(max_length = 50)
    region = models.CharField(max_length = 50)
    password = models.CharField(max_length = 200)

    class Meta:
        db_table = 'companies'

class Announcement(TimeStampModel):
    company = models.ForeignKey(Company, on_delete = models.CASCADE)
    title = models.CharField(max_length = 100)
    content = models.CharField(max_length = 10000)
    position = models.CharField(max_length = 100)
    compensation = models.DecimalField(max_digits = 13, decimal_places = 2)
    skill = models.CharField(max_length = 100)

    class Meta:
        db_table = 'announcements'