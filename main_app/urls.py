from django.urls import path, URLPattern
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/submit_profile/', views.profile_submit, name='profile_submit'),
    path('accounts/profile/update/', views.profile_update, name='profile_update'),
    path('accounts/profile/submit_update/', views.submit_profile_update, name='submit_profile_update'),
    path('accounts/profile/delete/', views.profile_delete, name='profile_delete'),
    path('about/',views.about, name='about'),
    path('search/', views.search, name='search'),
    path("agent/<int:user_id>/detail/", views.detail, name='detail'),

    path('listing/create/', views.create_listing, name='create_listing'),
    path('listing/submit/', views.submit_listing, name='submit_listing'),
    path('listing/<int:listing_id>/detail/', views.listing_detail, name='listing_detail'),
    path('listing/<int:listing_id>/update/', views.listing_update, name='listing_update'),
    path('listing/<int:listing_id>/submit_update/', views.listing_update_submit, name='listing_update_submit'),

    path('listing/<int:listing_id>/delete/', views.listing_delete, name='listing_delete'),
    path('listing/featured/', views.listing_featured, name='listing_featured'),

    path("agent/loggedin/", views.loggedin, name='loggedin'),
    path("agent/edit/", views.edit, name='edit'),

    path('account/bookmarks/', views.bookmarks, name='bookmarks'),
    path('account/add_bookmark/', views.add_bookmark, name='add_bookmark'),

    path('listings/<int:listing_id>/delete_photo/<int:listingphoto_id>/', views.delete_photo, name='delete_photo'),

    # Asscociate a Toy with a Cat (M:M)
    path('listing/<int:listing_id>/detail/add_bookmark/<int:real_estate_id>', views.add_bookmark, name='add_bookmark'),
    # Unasscociate a Toy with a Cat (M:M)
    path('listing/<int:listing_id>/detail/remove_bookmark/<int:real_estate_id>', views.remove_bookmark, name='remove_bookmark'),
]