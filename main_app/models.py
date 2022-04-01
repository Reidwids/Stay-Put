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
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    address = models.TextField(max_length=250)
    postalCode = models.CharField(max_length=7)
    price = models.IntegerField()
    buildingType = models.CharField(max_length=1, choices=BuildingTypes, default=BuildingTypes[0][0])
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    parkingSpots = models.IntegerField()
    sqft = models.IntegerField()
    listingDate = models.DateField('Listing Date')
    realtor = models.IntegerField()
    
class Photo(models.Model):
    url = models.CharField(max_length=200)
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for real_estate_id: {self.real_estate_id} @{self.url}"