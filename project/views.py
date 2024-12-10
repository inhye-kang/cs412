from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView, DeleteView, View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import login, authenticate
from .models import UserProfile, Review, LookupWine, Wine, Favorite
from .forms import CreateProfileForm, ReviewForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django_countries import countries
from django_countries.fields import CountryField
import logging
from math import pi
from django.conf import settings 
import requests
from django.http import JsonResponse
import os
from django.db.models import F
from django.http import HttpResponseRedirect
from random import sample
import pandas as pd


logger = logging.getLogger(__name__)

# ---------------------------------------------------------------
#                           Profile Views
# ---------------------------------------------------------------
    
class ShowProfileView(LoginRequiredMixin, DetailView):
    """
    Displays user profile with associated reviews and favorites.
    """
    model = UserProfile
    template_name = 'project/profile.html'
    context_object_name = 'profile'

    def get_login_url(self):
        """Return the login URL."""
        return reverse('login')

    def get_context_data(self, **kwargs):
        """
        Add reviews, favorites, and user details to context.
        """
        context = super().get_context_data(**kwargs)
        user_profile = get_object_or_404(UserProfile, pk=self.kwargs['pk'])

        # Fetch user reviews and favorites
        context['reviews'] = Review.objects.filter(user=self.object.user)
        context['favorites'] = Favorite.objects.filter(user=self.request.user).select_related('wine')
        reviews = Review.objects.filter(user=user_profile.user).select_related('wine').order_by('-created_at')

        # Filter reviews with valid coordinates
        reviews_with_location = list(reviews.filter(
            latitude__isnull=False, longitude__isnull=False
        ).values(
            'restaurant_name', 'latitude', 'longitude', 'rating', 'wine__name'
        ))

        # Update context with fetched data and make it JSON-safe for map API
        context.update({
            'reviews': reviews,
            'reviews_with_location': reviews_with_location,
            'is_own_profile': user_profile == self.request.user.userprofile,
        })

        return context

class CreateProfileView(CreateView):
    """
    Handles user profile creation.
    """
    form_class = CreateProfileForm
    template_name = 'project/create_new_profile_form.html'

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        """Save the user profile after successful form validation."""
        context = self.get_context_data()
        user_form = context['user_form']

        # Create and log in the new user
        if user_form.is_valid():
            user = user_form.save()
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(self.request, user)
            form.instance.user = user
            self.object = form.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm(self.request.POST)
        return context
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """
    Handles updating a user's profile.

    Allows logged-in users to edit their profile details 
    such as their username, email, profile image, and other personal information.

    """
    model = UserProfile
    form_class = CreateProfileForm
    template_name = 'project/update_profile.html'

    def get_object(self):
        """
        Retrieves the current user's profile and return the profile object linked to the logged-in user.
        """
        return UserProfile.objects.filter(user=self.request.user).first()

    def get_success_url(self):
        """
        Redirect user back to the profile page after a successful profile update.
        """
        return reverse('profile', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        """
        Return context data for the current user profile.
        """
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        return context
    

# ---------------------------------------------------------------
#                       Wine Review Views
# ---------------------------------------------------------------

class CreateWineReviewView(LoginRequiredMixin, CreateView):
    """
    Handles the creation of new wine reviews by authenticated users.

    Process form submissions for creating wine reviews and associating the review with the logged-in user.
    """
    model = Review
    form_class = ReviewForm
    template_name = 'project/create_wine_review.html'

    def get_success_url(self) -> str:
        """
        Redirects the user to the home page after a successful form submission.
        """
        return reverse('home')

    def form_valid(self, form):
        """
        Assigns the logged-in user to the review.
        Validates and creates or retrieves a wine record.
        Validates the presence of coordinates and restaurant name.

        Redirect to success URL if valid, form error if not.
        """
        form.instance.user = self.request.user

        # Extract form data
        wine_name = self.request.POST.get('wine_name', "").strip()
        varietal = self.request.POST.get('varietal', "").strip()
        country_of_origin = self.request.POST.get('country_of_origin', "").strip()
        restaurant_name = self.request.POST.get('restaurant_name', "").strip()
        latitude = self.request.POST.get('latitude')
        longitude = self.request.POST.get('longitude')

        # Debug: validate required fields
        logger.debug("Latitude: %s, Longitude: %s", latitude, longitude)
        if not restaurant_name:
                form.add_error('restaurant_name', 'Restaurant name cannot be empty.')
                return self.form_invalid(form)

        if not latitude or not longitude:
            form.add_error(None, "Please select a restaurant from the search results.")
            return self.form_invalid(form)

        if not wine_name:
            form.add_error('wine', 'Wine name cannot be empty.')
            return self.form_invalid(form)

        # Create or retrieve the wine
        wine = Wine.objects.get(
            name=wine_name,
            defaults={'varietal': varietal, 'country_of_origin': country_of_origin}
        )

        # Assign validated data to the form instance
        form.instance.wine = wine
        form.instance.varietal = varietal
        form.instance.restaurant_name = restaurant_name
        form.instance.latitude = float(latitude)
        form.instance.longitude = float(longitude)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Returns updated context and country data for dropdown menu.
        """
        context = super().get_context_data(**kwargs)
        context['countries'] = [(code, name) for code, name in countries]
        return context

class UpdateWineReviewView(LoginRequiredMixin, UpdateView):
    """
    Handles updating of existing wine reviews by authenticated users.

    Users can update details such as wine name, varietal, and restaurant data.
    """
    model = Review
    form_class = ReviewForm
    template_name = 'project/update_wine_review.html'

    def get_success_url(self):
        """
        Redirects to the user's profile page after a successful update.
        """
        return reverse('profile', kwargs={'pk': self.request.user.userprofile.pk})

    def form_valid(self, form):
        """
        Extracts form fields from the POST request.
        Retrieves/creates the associated wine record.
        Assigns review fields such as varietal, restaurant name, and location.
        Handles conversion errors when assigning latitude and longitude for the map API.
        Links the review instance to the logged-in user.

        Redirect to success URL if valid, form error if not.
        """
        # Extract form data from POST request
        wine_name = self.request.POST.get('wine_name', "").strip()
        varietal = self.request.POST.get('varietal', "").strip()
        country_of_origin = self.request.POST.get('country_of_origin', "").strip()
        restaurant_name = self.request.POST.get('restaurant_name', "").strip()
        latitude = self.request.POST.get('latitude', None)
        longitude = self.request.POST.get('longitude', None)

        # Validate wine name before processing
        if not wine_name:
            form.add_error('wine', 'Wine name cannot be empty.')
            return self.form_invalid(form)

        # Retrieve the wine record
        wine = Wine.objects.get(name=wine_name)
        form.instance.wine = wine # Link the wine instance

        # Assign form fields to the review instance
        form.instance.user = self.request.user
        form.instance.varietal = varietal
        form.instance.restaurant_name = restaurant_name
        form.instance.country_of_origin = country_of_origin

        # Validate and assign latitude and longitude
        try:
            form.instance.latitude = float(latitude) if latitude else None
            form.instance.longitude = float(longitude) if longitude else None
        except ValueError:
            form.add_error(None, "Invalid coordinates. Please try selecting a restaurant again.")
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Returns updated context and country data for dropdown menu.
        """
        context = super().get_context_data(**kwargs)
        context['countries'] = [(code, name) for code, name in countries]
        context['wine_name'] = self.object.wine.name if self.object.wine else ""
        context['varietal'] = self.object.varietal
        context['restaurant_name'] = self.object.restaurant_name
        context['latitude'] = self.object.latitude
        context['longitude'] = self.object.longitude

        return context
    
class DeleteWineReviewView(LoginRequiredMixin, DeleteView):
    """
    Handles deletion of wine reviews by users.

    Provides confirmation and deletes reviews in a separate page if users confirm the action.
    """
    model = Review
    template_name = 'project/delete_review_form.html'
    context_object_name = 'review'

    def get_success_url(self):
        """
        Redirects to the user's profile page after deletion.
        """
        profile = self.object.user.userprofile
        return reverse('profile', kwargs={'pk': profile.pk})

    def get_context_data(self, **kwargs):
        """
        Adds context data to the delete confirmation page and returns context with profile and current time data.
        """
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        context['profile'] = self.object.user.userprofile
        return context

    def get_profile_url(self) -> str:
        """Return the URL to the user's profile page."""
        profile = self.object.user.userprofile
        return reverse('profile', kwargs={'pk': profile.pk})
    
class FavoriteWineView(LoginRequiredMixin, View):
    """
    Manages wine favoriting and unfavoriting actions.

    Allows users to add or remove wines from their favorites list.
    """
    template_name = 'project/main_feed.html'

    def get_login_url(self):
        """Return the login URL."""
        return reverse('login')

    def post(self, request, wine_id, *args, **kwargs):
        """
        Handles POST requests to toggle wine favorite status in the review cards of the main feed.
        """
        action = request.POST.get("action")
        wine = get_object_or_404(Wine, pk=wine_id)

        if action == "favorite":
            Favorite.objects.get_or_create(user=request.user, wine=wine)
        elif action == "unfavorite":
            Favorite.objects.filter(user=request.user, wine=wine).delete()

        # Redirect to the same page
        return redirect(request.META.get("HTTP_REFERER", "home"))

    def get_context_data(self, **kwargs):
        """
        Adds reviews, favorites, and saved wines to the context.
        """
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.select_related('wine', 'user').order_by('-created_at')
        context['favorites'] = Favorite.objects.filter(user=self.request.user).values_list('wine_id', flat=True)
        
        # Correct query for saved wines using favorited_by
        context['saved_wines'] = Wine.objects.filter(favorited_by__user=self.request.user).distinct()

        # Add reviews with location for map
        reviews_with_location = Review.objects.filter(
            latitude__isnull=False, longitude__isnull=False
        ).values(
            "restaurant_name", "latitude", "longitude", "rating", "wine__name", "user__username"
        )
        context['reviews_with_location'] = list(reviews_with_location)
        return context
    

# ---------------------------------------------------------------
#                       Wine Search View
# ---------------------------------------------------------------

class WineLookupView(ListView):
    """Displays wine recommendations based on search filters from the imported wine data."""
    model = LookupWine
    template_name = 'project/wine_lookup.html'
    context_object_name = 'wines'
    paginate_by = 30

    def get_queryset(self):
        """Filter wines based on search parameters."""
        queryset = super().get_queryset()
        filters = {
            'category__iexact': self.request.GET.get('category'),
            'winery__icontains': self.request.GET.get('winery'),
            'price__gte': self.request.GET.get('min_price'),
            'price__lte': self.request.GET.get('max_price'),
            'rating__gte': self.request.GET.get('min_rating'),
            'alcohol__icontains': self.request.GET.get('alcohol_content'),
            'appellation__icontains': self.request.GET.get('country'),
        }
        for key, value in filters.items():
            if value:
                queryset = queryset.filter(**{key: value})

        sort_by = self.request.GET.get('sort_by', '')
        if sort_by:
            queryset = queryset.order_by(sort_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_choices'] = ['Red', 'Sparkling', 'White', 'Port/Sherry', 'Rose', 'Dessert', 'Fortified']

        # Only fetch wines if search parameters are present
        if any(
            self.request.GET.get(field)
            for field in ['category', 'min_price', 'max_price', 'min_rating', 'alcohol_content', 'country']
        ):
            filtered_wines = self.get_queryset()
            wine_list = list(filtered_wines)
            context['random_wines'] = sample(wine_list, min(len(wine_list), 5))
        else:
            context['random_wines'] = []

        # Form input persistence
        context.update({
            'category_search': self.request.GET.get('category', ''),
            'min_price': self.request.GET.get('min_price', ''),
            'max_price': self.request.GET.get('max_price', ''),
            'min_rating': self.request.GET.get('min_rating', ''),
            'alcohol_content': self.request.GET.get('alcohol_content', ''),
            'country_search': self.request.GET.get('country', ''),
        })
        return context

# ---------------------------------------------------------------
#                     Wine Review Feed View
# ---------------------------------------------------------------
class MainFeedView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'project/main_feed.html'
    context_object_name = 'reviews'

    def get_login_url(self) -> str:
        '''Return the URL to the login page.'''
        return reverse('login')

    def get_queryset(self):
        reviews = Review.objects.select_related('wine', 'user').order_by('-created_at')
        circumference = 2 * pi * 55  # Circle radius = 40
        for review in reviews:
            if review.rating is not None:
                review.stroke_dashoffset = circumference - (review.rating / 10) * circumference
            else:
                review.stroke_dashoffset = circumference
        return reviews

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites'] = Favorite.objects.filter(user=self.request.user).values_list('wine_id', flat=True)

        reviews_with_location = Review.objects.filter(
            latitude__isnull=False, longitude__isnull=False
        ).values(
            "restaurant_name", "latitude", "longitude", "rating", "wine__name", 'user__username'
        )
        
        context.update({
            'circle_radius': 26,  # Pass radius to template for ranking circle
            'reviews_with_location': list(reviews_with_location),
            'GOOGLE_API_KEY': settings.GOOGLE_API_KEY,
        })
        return context


# ---------------------------------------------------------------
#                    Google Places API Methods
# Description: These methods interact with the Google Places API
# to fetch autocomplete suggestions, place details, and official 
# website URLs for queried locations.
# ---------------------------------------------------------------

def google_places_autocomplete(request):
    """
    Fetches autocomplete suggestions from Google Places API based on user input.

    Args:
        request (HttpRequest): The incoming request containing the user's input text.

    Returns:
        JsonResponse: A JSON response containing autocomplete results or an error message.
    """

    input_text = request.GET.get('input', '').strip()
    if not input_text:
        return JsonResponse({"error": "Missing input text"}, status=400)

    api_key = settings.GOOGLE_API_KEY
    url = f'https://maps.googleapis.com/maps/api/place/autocomplete/json?input={input_text}&key={api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status() # Raise exception for HTTP errors

        return JsonResponse(response.json())
    
    except requests.exceptions.RequestException as e:

        return JsonResponse({"error": "Failed to fetch data from Google Places API"}, status=500)
    
def google_places_details(request):
    """
    Retrieves detailed information for a specific place using its Place ID from Google Places API.

    Args:
        request (HttpRequest): The incoming request containing the Place ID.

    Returns:
        JsonResponse: A JSON response with location details or an error message.
    """

    place_id = request.GET.get("place_id")

    # Validate the existence of Place ID
    if not place_id:
        return JsonResponse({"error": "Missing place_id"}, status=400)

    api_key = settings.GOOGLE_API_KEY
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        details = response.json()

        print("Google Places Details Response:", details)  # Debug output

        # Extract and return relevant location details
        if (
            "result" in details 
            and "geometry" in details["result"] 
            and "location" in details["result"]["geometry"]
        ):
            location = details["result"]["geometry"]["location"]

            return JsonResponse(location)
        
        else:
            # Handle for unexpected API responses
            return JsonResponse(
                {"error": "Invalid API response", "details": details}, status=500
            )
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": "Failed to fetch data from Google Places API"}, status=500)

def get_place_website(request):
    """
    Retrieves a place's official website URL from Google Places API based on its name.

    Args:
        request (HttpRequest): The incoming request containing the place name.

    Returns:
        JsonResponse: A JSON response containing the website URL or an error message.
    """

    # Extract place name
    place_name = request.GET.get("place_name", "")
    api_key = settings.GOOGLE_API_KEY

    if not place_name:
        return JsonResponse({"error": "Missing place_name"}, status=400)

    try:
        # Find the Place ID using Google Places API
        find_place_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        find_place_params = {
            "input": place_name,
            "inputtype": "textquery",
            "fields": "place_id",
            "key": api_key,
        }

        # Make  request and extract Place ID
        find_place_response = requests.get(find_place_url, params=find_place_params).json()
        place_id = find_place_response.get("candidates", [{}])[0].get("place_id")

        if not place_id:
            return JsonResponse({"website": "Website not available"})

        # Fetch place details and the website URL
        place_details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        place_details_params = {
            "place_id": place_id,
            "fields": "website,name,formatted_address,rating,geometry",
            "key": api_key,
        }

        place_details_response = requests.get(place_details_url, params=place_details_params).json()
        website = place_details_response.get("result", {}).get("website", "Website not available")

        # Return the website URL
        return JsonResponse({"website": website})

    except Exception as e:
        logger.error(f"Error fetching place details: {str(e)}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)

def load_wine_data():
    session = boto3.session.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_S3_REGION_NAME"),
    )
    s3 = session.resource('s3')
    obj = s3.Object('project-wine-data-cs412', 'winedata.csv')
    data = obj.get()['Body'].read().decode('utf-8')

    # Load CSV into pandas DataFrame
    df = pd.read_csv(pd.compat.StringIO(data))
    return df