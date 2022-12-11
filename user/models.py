from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=256)
    age = models.IntegerField(null=True)
    months = models.CharField(max_length=200)
    slot = models.CharField(max_length=20)
