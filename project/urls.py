# urls.py
from django.urls import path
from .views import (
    CreateProfileView, ShowProfileView, UpdateWineReviewView, 
    MainFeedView, WineLookupView, UpdateProfileView,  CreateWineReviewView, 
    DeleteWineReviewView, FavoriteWineView
)
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # --- Home & Authentication ---
    path('', MainFeedView.as_view(), name='home'),
    path('login/', LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # --- Profile ---
    path('create_new_profile/', CreateProfileView.as_view(), name='create_new_profile'),
    path('profile/<int:pk>/', ShowProfileView.as_view(), name='profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),

    # --- Wine Reviews ---
    path('create_wine_review/', CreateWineReviewView.as_view(), name='create_wine_review'),
    path('profile/update-review/<int:pk>/', UpdateWineReviewView.as_view(), name='update_wine_review'),
    path('review/delete/<int:pk>/', DeleteWineReviewView.as_view(), name='delete_review'),
    path('favorite_toggle/<int:wine_id>/', FavoriteWineView.as_view(), name='favorite_toggle'),

    # --- Wine Lookup ---
    path('wine_lookup/', WineLookupView.as_view(), name='wine_lookup'),

    # --- Google Places API ---
    path("google-places-autocomplete/", views.google_places_autocomplete, name="google_places_autocomplete"),
    path("google-places-details", views.google_places_details, name="google_places_details"),
    path('get_place_website/', views.get_place_website, name='get_place_website'),
]
