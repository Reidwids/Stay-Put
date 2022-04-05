from django.shortcuts import render, redirect
from .models import Profile, RealEstate, ListingPhoto, ProfilePhoto
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
    try:
        profile = Profile.objects.get(user=request.user)
        photo_url = ProfilePhoto.objects.get(profile=request.user.id).url
        print(photo_url)
        return render(request, 'agent/profile.html', {'profile': profile, 'photo_url': photo_url})
    except:
        return render(request, 'agent/create_profile.html')

def profile_submit(request):
    new_profile = Profile(
        firstName = request.POST['firstName'],
        lastName = request.POST['lastName'],
        licenseNumber = request.POST['licenseNumber'],
        phoneNumber = request.POST['phoneNumber'],
        email = request.POST['email'],
        isAgent = True,
        isAdmin = False,
        user = request.user,
        )
    new_profile.save()
    photo_file = request.FILES.get('image', None)
    photo_url = ''
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"https://{BUCKET}.{S3_BASE_URL}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = ProfilePhoto(url=url, profile_id = new_profile.user_id)
            photo.save()
            photo_url = photo.url
        except:
            print('An error occurred uploading file to S3')
    else: 
        photo = ProfilePhoto(url='https://stay-put.s3.ca-central-1.amazonaws.com/af7588.jpg', profile_id = new_profile.user_id)
        photo.save()
        photo_url = photo.url
    # return redirect('profile', {'profile': new_profile,  'photo_url': photo_url})
    return render(request, 'agent/profile.html', {'profile': new_profile,  'photo_url': photo_url})

def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    photo_url = ProfilePhoto.objects.get(profile=request.user.id).url
    return render(request, 'agent/update_profile.html', {'profile': profile, 'photo_url': photo_url})

def submit_profile_update(request):
    profile = Profile.objects.filter(user=request.user)
    profile.update(firstName = request.POST['firstName'])
    profile.update(lastName = request.POST['lastName'])
    profile.update(licenseNumber = request.POST['licenseNumber'])
    profile.update(phoneNumber = request.POST['phoneNumber'])
    profile.update(email = request.POST['email'])
    photo_file = request.FILES.get('image', None)
    old_key = ProfilePhoto.objects.get(profile = request.user.id).url
    old_key = old_key.replace(f"https://{BUCKET}.{S3_BASE_URL}/","")
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        
        if old_key != 'af7588.jpg':
            s3.delete_object(Bucket = BUCKET, Key = old_key)
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"https://{BUCKET}.{S3_BASE_URL}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            profile = ProfilePhoto.objects.filter(profile = request.user.id)
            profile.update(url=url)
        except:
            print('An error occurred uploading file to S3')
    return redirect('profile')

def profile_delete(request):
    Profile.objects.filter(user=request.user).delete()
    return redirect('profile')

def user_delete(request):
    pass
    

def detail(request,user_id):
    agent=Profile.objects.get(user_id=user_id)
    agent.image = ProfilePhoto.objects.get(profile_id=agent.user_id)
    return render(request,'agent/detail.html',{'agent':agent})

def loggedin(request):
    return render(request,'agent/loggedin.html')

def edit(request):
    return render(request,'agent/edit.html') 

def about(request):
    realtors = Profile.objects.all()
    for realtor in realtors:
         realtor.profilePhoto = ProfilePhoto.objects.get(profile_id=realtor.user_id)
    return render(request,'about.html',{'realtors': realtors[:6]})

def search(request):
    listings = RealEstate.objects.all()
    if request.POST['province']:
        listings = listings.filter(province=request.POST['province'])
    if request.POST['city']:
        listings = listings.filter(city=request.POST['city'])
    # if request.POST['postalCode']:
    #     listings = listings.filter(postalCode=request.POST['postalCode'])
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
        listing_with_photo.append([listing, ListingPhoto.objects.filter(real_estate=listing.id)[0].url])
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

    if photo_files:
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
                photo = ListingPhoto(url=url, real_estate_id = new_listing.id)
                photo.save()
                print(photo)
            except:
                print('An error occurred uploading file to S3')
    else: 
        photo = ListingPhoto(url='https://stay-put.s3.ca-central-1.amazonaws.com/49fe05.jpg', real_estate_id = new_listing.id)
        photo.save()
    return render(request, 'agent/profile.html')
    
    
def listing_detail(request, listing_id):
    listing = RealEstate.objects.get(id=listing_id)
    listing.buildingType = listing.get_buildingType_display()
    listing.parking = listing.get_parking_display()
    agent = Profile.objects.get(user_id=listing.realtor_id)
    return render(request,'listing/detail.html', {'listing': listing, 'agent': agent})

def listing_featured(request):
    listings=RealEstate.objects.all()
    return render(request,'listing/featured.html',{'listings': listings})

def listing_update(request):
    print(request)

def listing_delete(request):
    print(request)