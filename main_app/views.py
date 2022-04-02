from django.shortcuts import render, redirect
from .models import Profile, RealEstate, Photo
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import uuid
import boto3
S3_BASE_URL = 'https://s3.ca-central-1.amazonaws.com'
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
    return render(request,'about.html')

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
    if request.POST['max_sqft']:
        listings = listings.filter(sqft__lt=request.POST['max_sqft'])
        
    # if request.POST['realtor']:
    #     listings = listings.filter(price__gt=request.POST['realtor'])
    # if request.POST['listing_date']:
    #     listings = listings.filter(sqft__gt=request.POST['min_sqft'])
    # if request.POST['closing_date']:
    #     listings = listings.filter(sqft__lt=request.POST['max_sqft'])
    print(listings)
    return render(request, 'search.html', {'listings': listings})

def create_listing(request):
    return render(request, 'listing/create_listing.html')

def submit_listing(request):
    photo_files = request.FILES.getlist('images', None)
    for photo_file in photo_files:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, real_estate_id = request.user.id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    
    
    return redirect('profile')
    
    

def listing_detail(request):
    print(request)

def listing_update(request):
    print(request)

def listing_delete(request):
    print(request)