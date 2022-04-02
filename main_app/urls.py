from django.urls import path, URLPattern
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/create/', views.ProfileCreate.as_view(), name='profile_create'),
    path('accounts/profile/<int:pk>/update/', views.ProfileUpdate.as_view(), name='profile_update'),
    path('about/',views.about, name='about'),
    path("agent/detail/", views.detail, name='detail')
]