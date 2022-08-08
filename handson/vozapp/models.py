from django.db import models

# Create your models here.
from django.db import models


class Employee(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=120)
    salary = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'employee'
