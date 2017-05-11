from django.db import models


class Shape(models.Model):
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)


class Address(models.Model):
    id = models.BigIntegerField
    shape = Shape
    street = models.CharField(max_length=40)
    street_noaccents = models.CharField(max_length=40)
    houseNumber = models.CharField(max_length=30)
    landRegistryNumber = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
