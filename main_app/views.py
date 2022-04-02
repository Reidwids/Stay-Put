from django.shortcuts import render, redirect
from .models import Profile, RealEstate
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

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
    profile = Profile.objects.get(user=request.user)
    # print(profile.firstName)
    return render(request, 'agent/profile.html', {'profile': profile})

def detail(request):
    return render(request,'agent/detail.html')

class ProfileCreate(CreateView):
    model = Profile
    fields = ['firstName', 'lastName', 'image', 'licenseNumber', 'phoneNumber', 'email']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProfileUpdate(UpdateView):
    model = Profile
    fields = ['firstName', 'lastName', 'image', 'licenseNumber', 'phoneNumber', 'email']
    success_url = '/accounts/profile'
def about(request):
    return render(request,'about.html')
