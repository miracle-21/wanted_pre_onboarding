from django.db import models

class Company(models.Model):
    name = models.CharField(max_length = 100)
    nation = models.CharField(max_length = 50)
    region = models.CharField(max_length = 50)
    password = models.CharField(max_length = 200)

    class Meta:
        db_table = 'companies'