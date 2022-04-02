from xmlrpc.client import DateTime
from django.db import models
import datetime
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

BuildingTypes = (
    ('C', 'Condo'),
    ('T', 'Townhouse'),
    ('S', 'Semi-Detached'),
    ('H', 'House')
)

Provinces = (
    ('Ontario', 'Ontario'),
    ('Prince Edward Island', 'Prince Edward Island'),
    ('Nova Scotia', 'Nova Scotia'),
    ('New Brunswick', 'New Brunswick'),
    ('Newfoundland and Labrador', 'Newfoundland and Labrador'),
    ('Quebec', 'Quebec'),
    ('Winnipeg', 'Winnipeg'),
    ('Saskatchewan', 'Saskatchewan'),
    ('Alberta', 'Alberta'),
    ('British Columbia', 'British Columbia'),
    ('Yukon', 'Yukon'),
    ('Northwest Territories', 'Northwest Territories'),
    ('Nunavut', 'Nunavut'),
)
Parking = (
    ('Y', 'Yes'),
    ('N', 'No'),
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
    province = models.CharField(max_length=50, choices=Provinces, default=Provinces[0][0])
    city = models.CharField(max_length=20)
    address = models.TextField(max_length=250)
    postalCode = models.CharField(max_length=7)
    price = models.IntegerField()
    buildingType = models.CharField(max_length=1, choices=BuildingTypes, default=BuildingTypes[0][0])
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    parking = models.CharField(max_length=1, choices=Parking, default=Parking[0][0])
    sqft = models.IntegerField()
    listingDate = models.DateField('Listing Date')
    closingDate = models.DateField('Closing Date')
    realtor = models.IntegerField()
    
class Photo(models.Model):
    url = models.CharField(max_length=200)
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for real_estate_id: {self.real_estate_id} @{self.url}"