from django.shortcuts import render, redirect
from .models import Profile, RealEstate, Photo
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from datetime import date
import uuid
import boto3
S3_BASE_URL = 's3.ca-central-1.amazonaws.com'
BUCKET = 'stay-put'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # save the user to the database
            user = form.save()
            # login the user
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid signup - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def profile(request):
    if Profile.objects.filter(user=request.user):
        profile = Profile.objects.get(user=request.user)
    else:
        profile = Profile.objects.filter(user=request.user)
    return render(request, 'agent/profile.html', {'profile': profile})

def detail(request):
    return render(request,'agent/detail.html')

def loggedin(request):
    return render(request,'agent/loggedin.html')

def edit(request):
    return render(request,'agent/edit.html')

def listingDetail(request):
    return render(request,'listing/detail.html')

class ProfileCreate(CreateView):
    model = Profile
    fields = ['firstName', 'lastName', 'image', 'licenseNumber', 'phoneNumber', 'email']
    success_url = '/accounts/profile'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProfileUpdate(UpdateView):
    model = Profile
    fields = ['firstName', 'lastName', 'image', 'licenseNumber', 'phoneNumber', 'email']
    success_url = '/accounts/profile'

def about(request):
    realtors = Profile.objects.all()
    realtor_length= len(realtors)
    return render(request,'about.html',{'realtors': realtors[:7], 'length': realtor_length})

def search(request):
    listings = RealEstate.objects.all()
    if request.POST['province']:
        listings = listings.filter(province=request.POST['province'])
    if request.POST['city']:
        listings = listings.filter(city=request.POST['city'])
    if request.POST['postalCode']:
        listings = listings.filter(postalCode=request.POST['postalCode'])
    if request.POST['min_price']:
        listings = listings.filter(price__gt=request.POST['min_price'])
    if request.POST['max_price']:
        listings = listings.filter(price__lt=request.POST['max_price'])
    if request.POST['buildingType']:
        listings = listings.filter(buildingType=request.POST['buildingType'])
    if request.POST['bedrooms']:
        listings = listings.filter(bedrooms=request.POST['bedrooms'])
    if request.POST['bathrooms']:
        listings = listings.filter(bathrooms=request.POST['bathrooms'])
    if request.POST['parking']:
        listings = listings.filter(parking=request.POST['parking'])
    if request.POST['min_sqft']:
        listings = listings.filter(sqft__gt=request.POST['min_sqft'])
    
    # if request.POST['realtor']:
    #     listings = listings.filter(price__gt=request.POST['realtor'])
    # if request.POST['listing_date']:
    #     listings = listings.filter(sqft__gt=request.POST['listing_date'])
    # if request.POST['closing_date']:
    #     listings = listings.filter(sqft__lt=request.POST['closing_date'])
    listing_with_photo = []
    for listing in listings:
        listing_with_photo.append([listing, Photo.objects.filter(real_estate=listing.id)[0].url])
    for listing in listing_with_photo:
        print(listing[1])
    return render(request, 'search.html', {'listing_with_photo': listing_with_photo})

def create_listing(request):
    return render(request, 'listing/create_listing.html')

def submit_listing(request):
    today = date.today()
    date_format = today.strftime("%Y-%m-%d")

    new_listing = RealEstate(
        province = request.POST['province'],
        city = request.POST['city'],
        address = request.POST['address'],
        postalCode = request.POST['postalCode'],
        price = request.POST['price'],
        buildingType = request.POST['buildingType'],
        bedrooms = request.POST['bedrooms'],
        bathrooms = request.POST['bathrooms'],
        parking = request.POST['parking'],
        sqft = request.POST['sqft'],
        listingDate = date_format,
        closingDate = request.POST['closingDate'],
        realtor_id = request.user.id,
        description = request.POST['description'],
    )
    new_listing.save()
    photo_files = request.FILES.getlist('images', None)
    for photo_file in photo_files:
        print(photo_file)
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"https://{BUCKET}.{S3_BASE_URL}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, real_estate_id = new_listing.id)
            photo.save()
            print(photo)
        except:
            print('An error occurred uploading file to S3')
    return render(request, 'agent/profile.html')
    
    

def listing_detail(request):
    print(request)

def listing_update(request):
    print(request)

def listing_delete(request):
    print(request)