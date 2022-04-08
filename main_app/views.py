from django.shortcuts import render, redirect
from .models import Bookmark, Profile, RealEstate, ListingPhoto, ProfilePhoto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required 
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
            return redirect('/accounts/profile/')
        else:
            error_message = 'Invalid signup - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@login_required
def bookmarks(request):
    profile = Profile.objects.get(user=request.user)
    bookmarks = Bookmark.objects.filter(real_estate_id__in = profile.bookmarks.all().values_list('real_estate_id'))
    print(bookmarks)
    alllistings = RealEstate.objects.all()
    listings = []
    for bookmark in bookmarks:
        listing = alllistings.get(id=bookmark.real_estate_id)
        listings.append(listing)
    listing_with_photo = []
    for listing in listings:
        listing_with_photo.append([listing, ListingPhoto.objects.filter(real_estate=listing.id)[0].url])
    for listing in listing_with_photo:
        print(listing[1])
    return render(request, 'bookmarks.html', {'listing_with_photo': listing_with_photo})


@login_required
def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
        current_user = Profile.objects.get(user=request.user)
        photo_url = ProfilePhoto.objects.get(profile=request.user.id).url
        listings = RealEstate.objects.filter(realtor_id=profile.user_id)
        listing_with_photo = []
        for listing in listings:
            photo_urls = ListingPhoto.objects.filter(real_estate_id=listing.id)
            listing.photo_url = photo_urls[0].url
            listing_with_photo.append([listing, ListingPhoto.objects.filter(real_estate=listing.id)[0].url])
            print(listing_with_photo)
        return render(request, 'agent/profile.html', {'profile': profile, 'photo_url': photo_url, 'listings': listings, 'listing_with_photo': listing_with_photo, 'current_user': current_user})
    except:
        print("Why is this working")
        return render(request, 'agent/create_profile.html')

@login_required
def profile_submit(request):
    new_profile = Profile(
        firstName = request.POST['firstName'],
        lastName = request.POST['lastName'],
        licenseNumber = request.POST['licenseNumber'],
        phoneNumber = request.POST['phoneNumber'],
        email = request.POST['email'],
        blurb = request.POST['blurb'],
        isAgent = False,
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
        photo = ProfilePhoto(url='https://stay-put.s3.ca-central-1.amazonaws.com/profile-placeholder.jpg', profile_id = new_profile.user_id)
        photo.save()
        photo_url = photo.url
    # return redirect('profile', {'profile': new_profile,  'photo_url': photo_url})
    return redirect("/accounts/profile/")

@login_required
def beanagent(request):
    profile=Profile.objects.get(user=request.user)
    profile.isAgent = True
    profile.save()
    return redirect('profile')

@login_required
def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    photo_url = ProfilePhoto.objects.get(profile=request.user.id).url
    return render(request, 'agent/update_profile.html', {'profile': profile, 'photo_url': photo_url})

@login_required
def submit_profile_update(request):
    profile = Profile.objects.filter(user=request.user)
    profile.update(firstName = request.POST['firstName'])
    profile.update(lastName = request.POST['lastName'])
    profile.update(licenseNumber = request.POST['licenseNumber'])
    profile.update(phoneNumber = request.POST['phoneNumber'])
    profile.update(email = request.POST['email'])
    profile.update(blurb = request.POST['blurb'])
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

@login_required
def profile_delete(request):
    Profile.objects.filter(user=request.user).delete()
    return redirect('profile')

def user_delete(request):
    pass
    
def detail(request, user_id):
    agent=Profile.objects.get(user_id=user_id)
    agent.image = ProfilePhoto.objects.get(profile_id=agent.user_id)
    listings = RealEstate.objects.filter(realtor_id=agent.user_id)
    for listing in listings:
        photo_urls = ListingPhoto.objects.filter(real_estate_id=listing.id)
        listing.photo_url = photo_urls[0].url
    return render(request,'agent/detail.html',{'agent':agent, 'listings': listings})

def loggedin(request):
    return render(request,'agent/loggedin.html')

@login_required
def edit(request):
    return render(request,'agent/edit.html') 

def about(request):
    realtors = Profile.objects.all().filter(isAgent=True)
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
    return render(request, 'search.html', {'listing_with_photo': listing_with_photo})

@login_required
def create_listing(request):
    currentUser = Profile.objects.get(user_id=request.user)
    return render(request, 'listing/create_listing.html', {'currentUser': currentUser})

@login_required
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
    new_bookmark = Bookmark(real_estate_id=new_listing.id)
    new_bookmark.save()
    photo_files = request.FILES.getlist('images', None)

    for photo_file in photo_files:
        if photo_file:
            print(photo_file)
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
            # just in case something goes wrong
            try:
                s3.upload_fileobj(photo_file, BUCKET, key)
                # build the full url string
                url = f"https://{BUCKET}.{S3_BASE_URL}/{key}"
                print(url)
                # we can assign to cat_id or cat (if you have a cat object)
                photo = ListingPhoto(url=url, real_estate_id = new_listing.id)
                photo.save()
                print(photo)
            except:
                print('An error occurred uploading file to S3')
        else: 
            photo = ListingPhoto(url='https://stay-put.s3.ca-central-1.amazonaws.com/propertyPlaceholder.jpg', real_estate_id = new_listing.id)
            photo.save()
    return redirect('/accounts/profile/')
    
    
def listing_detail(request, listing_id):
    listing = RealEstate.objects.get(id=listing_id)
    listing.buildingType = listing.get_buildingType_display()
    listing.parking = listing.get_parking_display()
    agent = Profile.objects.get(user_id=listing.realtor_id)
    agent.image = ProfilePhoto.objects.get(profile_id=agent.user_id)
    photo_urls = ListingPhoto.objects.filter(real_estate_id=listing.id)
    bookmark = Bookmark.objects.get(real_estate_id=listing_id)
    
    
    is_user_realtor = False
    if request.user.is_authenticated:
        currentUser = Profile.objects.get(user=request.user)
        userbookmarks=currentUser.bookmarks.values_list('real_estate_id', flat=True)
        is_user_realtor = True if agent.user_id == currentUser.user_id else False
        return render(request,'listing/detail.html', {'listing': listing, 'agent': agent, 'photo_urls': photo_urls, 'is_user_realtor': is_user_realtor, 'bookmark': bookmark, "userbookmarks": userbookmarks})
    return render(request,'listing/detail.html', {'listing': listing, 'agent': agent, 'photo_urls': photo_urls, 'is_user_realtor': is_user_realtor})

@login_required
def listing_update(request, listing_id):
    listing = RealEstate.objects.get(id=listing_id)
    photo_urls = ListingPhoto.objects.filter(real_estate_id=listing.id)
    agent = Profile.objects.get(user_id=listing.realtor_id)
    if request.user.is_authenticated:
        user = Profile.objects.get(user_id=request.user)
        is_user_realtor = True if listing.realtor_id == user.user_id else False 
    return render(request, 'listing/update_listing.html', {'is_user_realtor': is_user_realtor, 'listing': listing, 'agent': agent, 'photo_urls': photo_urls})

def agent_profile(request, agent_id):
    try:
        profile = Profile.objects.get(user_id=agent_id)
        photo_url = ProfilePhoto.objects.get(profile=agent_id).url
        listings = RealEstate.objects.filter(realtor_id=profile.user_id)
        listing_with_photo = []
        for listing in listings:
            photo_urls = ListingPhoto.objects.filter(real_estate_id=listing.id)
            listing.photo_url = photo_urls[0].url
            listing_with_photo.append([listing, ListingPhoto.objects.filter(real_estate=listing.id)[0].url])
        if request.user.is_authenticated:
            current_user = Profile.objects.get(user_id=request.user.id)
            return render(request, 'agent/profile.html', {'profile': profile, 'photo_url': photo_url, 'listings': listings, 'listing_with_photo': listing_with_photo, 'current_user': current_user})
        elif not request.user.is_authenticated:
            return render(request, 'agent/profile.html', {'profile': profile, 'photo_url': photo_url, 'listings': listings, 'listing_with_photo': listing_with_photo})
    except:
        print("Why is this working")
        return render(request, 'agent/create_profile.html')

def listing_featured(request):
    listings=RealEstate.objects.all()
    listing_with_photo = []
    photo_length=[]
    for listing in listings:
        photo_length.append(len(ListingPhoto.objects.filter(real_estate=listing.id)))
        listing_with_photo.append([listing, ListingPhoto.objects.filter(real_estate=listing.id),photo_length])
    
    return render(request, 'listing/featured.html', {'listing_with_photo': listing_with_photo})
    # return render(request,'listing/featured.html',{'listings': listings})

@login_required
def listing_update_submit(request, listing_id):
    if request.user.is_authenticated:
        user = Profile.objects.get(user_id=request.user)
        listing = RealEstate.objects.get(id=listing_id)
        is_user_realtor = True if listing.realtor_id == user.user_id else False 
        if is_user_realtor:
            listing = RealEstate.objects.filter(id=listing_id)
            listing.update(province = request.POST['province'])
            listing.update(city = request.POST['city'])
            listing.update(address = request.POST['address'])
            listing.update(postalCode = request.POST['postalCode'])
            listing.update(price = request.POST['price'])
            listing.update(buildingType = request.POST['buildingType'])
            listing.update(bedrooms = request.POST['bedrooms'])
            listing.update(bathrooms = request.POST['bathrooms'])
            listing.update(parking = request.POST['parking'])
            listing.update(sqft = request.POST['sqft'])
            listing.update(closingDate = request.POST['closingDate'])
            listing.update(description = request.POST['description'])
            listing.update(province = request.POST['province'])
            photo_urls = request.FILES.getlist('images', None)
            if photo_urls:
                for photo_url in photo_urls:
                    # old_keys = ListingPhoto.objects.filter(real_estate = listing_id)
                    # ##check following line if old_key can replace old_keys[i] 
                    # old_key = old_keys[i].url.replace(f"https://{BUCKET}.{S3_BASE_URL}/","")
                    s3 = boto3.client('s3')
                    key = uuid.uuid4().hex[:6] + photo_url.name[photo_url.name.rfind('.'):]
                    # just in case something goes wrong
                    
                    # if old_key != '49fe05.jpg':
                    #     s3.delete_object(Bucket = BUCKET, Key = old_key)
                    try:
                        s3.upload_fileobj(photo_url, BUCKET, key)
                        # build the full url string
                        url = f"https://{BUCKET}.{S3_BASE_URL}/{key}"
                        # we can assign to cat_id or cat (if you have a cat object)
                        photo = ListingPhoto(url=url, real_estate_id = listing_id)
                        photo.save()
                    except:
                        print('An error occurred uploading file to S3')
    return redirect('listing_detail', listing_id=listing_id)

@login_required
def listing_delete(request, listing_id):
    if request.user.is_authenticated:
        user = Profile.objects.get(user_id=request.user)
        listing = RealEstate.objects.get(id=listing_id)
        is_user_realtor = True if listing.realtor_id == user.user_id else False 
        if is_user_realtor:
            old_keys = ListingPhoto.objects.filter(real_estate = listing_id)
            for old_key in old_keys:
                old_key = old_key.url.replace(f"https://{BUCKET}.{S3_BASE_URL}/","")
                s3 = boto3.client('s3')        
                if old_key != '49fe05.jpg':
                    s3.delete_object(Bucket = BUCKET, Key = old_key)
            RealEstate.objects.filter(id=listing_id).delete()
    return redirect('profile')

@login_required
def delete_photo(request, listing_id, listingphoto_id):
    if request.user.is_authenticated:
        user = Profile.objects.get(user_id=request.user)
        listing = RealEstate.objects.get(id=listing_id)
        is_user_realtor = True if listing.realtor_id == user.user_id else False 
        if is_user_realtor:
            old_key = ListingPhoto.objects.get(id= listingphoto_id)
            print(old_key.url)
            ListingPhoto.objects.get(id = listingphoto_id)
            s3 = boto3.client('s3')
            old_key = old_key.url.replace(f"https://{BUCKET}.{S3_BASE_URL}/","")
            print(BUCKET, old_key)
            s3.delete_object(Bucket = BUCKET, Key = old_key)
            ListingPhoto.objects.get(id= listingphoto_id).delete()
    return redirect('listing_update', listing_id=listing_id)


def add_bookmark(request, listing_id):
    user = Profile.objects.get(user_id=request.user)
    user.bookmarks.add(listing_id)
    return redirect('listing_detail', listing_id=listing_id)

def remove_bookmark(request, listing_id):
    user = Profile.objects.get(user_id=request.user)
    user.bookmarks.remove(listing_id)
    return redirect('listing_detail', listing_id=listing_id)

def terms_conditions(request):
    return render(request,'terms.html')