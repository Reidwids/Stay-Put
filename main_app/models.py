from django.db import models

# Create your models here.

BuildingTypes = (
    ('C', 'Condo'),
    ('T', 'Townhouse'),
    ('S', 'Semi-Detached'),
    ('H', 'House')
)

class User(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    image = models.CharField(default=None, blank=True, null=True, max_length=2000)
    licenseNumber = models.IntegerField()
    phoneNumber = models.IntegerField()
    email = models.EmailField()
    isAgent = models.BooleanField(default = True)
    isAdmin = models.BooleanField(default = False)

class RealEstate(models.Model):
    city = models.CharField(max_length=20)
    address = models.TextField(max_length=250)
    PRICE = models.IntegerField()
    buildingType = models.CharField(max_length=1, choices=BuildingTypes, default=BuildingTypes[0][0])
