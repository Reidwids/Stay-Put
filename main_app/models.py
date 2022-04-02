from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

BuildingTypes = (
    ('C', 'Condo'),
    ('T', 'Townhouse'),
    ('S', 'Semi-Detached'),
    ('H', 'House')
)

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    image = models.CharField(default=None, blank=True, null=True, max_length=2000)
    licenseNumber = models.IntegerField()
    phoneNumber = models.IntegerField()
    email = models.EmailField()
    isAgent = models.BooleanField(default = True)
    isAdmin = models.BooleanField(default = False)
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.user_id})

    def __str__(self):
        name = f"{self.firstName} {self.lastName}" 
        return name

class RealEstate(models.Model):
    city = models.CharField(max_length=30)
    address = models.TextField(max_length=250)
    PRICE = models.IntegerField()
    buildingType = models.CharField(max_length=1, choices=BuildingTypes, default=BuildingTypes[0][0])
