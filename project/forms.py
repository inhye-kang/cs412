from django import forms
from .models import UserProfile, Wine, Review, LookupWine
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    """
    Form for creating or updating user profiles.

    Fields:
    - first_name: User's first name.
    - last_name: User's last name.
    - email: Email address of the user.
    - city: City where the user resides (optional).
    - image_url: URL of the user's profile picture (optional).
    """
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'city', 'image_url']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'city': 'City',
            'image_url': 'Profile Picture (URL)',
        }
        # Widgets for customizing the HTML input elements for form fields
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

class CreateProfileForm(forms.ModelForm):
    """
    Form used for creating new user profiles.

    Fields:
    - Same as UserProfileForm.
    """
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'city', 'image_url']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'city': 'City',
            'image_url': 'Profile Picture (URL)',
        }
        # Widgets for customizing the HTML input elements for form fields
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

class WineForm(forms.ModelForm):
    """
    Form for managing Wine details.

    Fields:
    - name: The wine's name.
    - winery: The winery that produced the wine (optional).
    - category: The wine's type/category (optional).
    - varietal: Grape variety used (optional).
    - appellation: Geographic origin (optional).
    - alcohol: Alcohol content (optional).
    - price: The wine's price (optional).
    - rating: The wine's rating (optional).
    - reviewer: The person who reviewed the wine (optional).
    - review: Detailed review text (optional).
    """
    class Meta:
        model = Wine
        fields = [
            'name',
            'winery',
            'category',
            'varietal',
            'appellation',
            'alcohol',
            'price',
            'rating',
            'reviewer',
            'review',
        ]
        labels = {
            'name': 'Wine Name',
            'winery': 'Winery',
            'category': 'Category',
            'varietal': 'Varietal',
            'appellation': 'Appellation',
            'alcohol': 'Alcohol Content (%)',
            'price': 'Price',
            'rating': 'Rating',
            'reviewer': 'Reviewer',
            'review': 'Review',
        }
        # Widgets for customizing the HTML input elements for form fields
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'winery': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'varietal': forms.TextInput(attrs={'class': 'form-control'}),
            'appellation': forms.TextInput(attrs={'class': 'form-control'}),
            'alcohol': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100}),
            'reviewer': forms.TextInput(attrs={'class': 'form-control'}),
            'review': forms.Textarea(attrs={'class': 'form-control'}),
        }

# Review Form
class ReviewForm(forms.ModelForm):
    """
    Form for submitting or updating a wine review.

    Fields:
    - wine_name: Wine's name input from the user.
    - varietal: Grape varietal associated with the review.
    - wine: Reference to the Wine object being reviewed.
    - image_url: Optional image associated with the review.
    - country_of_origin: Country where the wine originates.
    - review_text: Detailed text content of the review.
    - rating: Overall wine rating out of 10.
    - body_rating: Rating for the wine's body out of 10.
    - finish_rating: Rating for the wine's finish out of 10.
    - taste_rating: Rating for the wine's taste out of 10.
    - restaurant_name: Name of the restaurant where the wine was tasted.
    - latitude: Restaurant's geographic latitude (hidden).
    - longitude: Restaurant's geographic longitude (hidden).
    """
    wine_name = forms.CharField(max_length=255, required=True)
    varietal = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Review
        fields = [
            'wine', 'image_url', 'country_of_origin', 
            'review_text', 'rating', 'body_rating', 
            'finish_rating', 'taste_rating', 'restaurant_name', 'latitude', 'longitude'
        ]
        # Widgets for customizing the HTML input elements for form fields
        widgets = {
            'review_text': forms.Textarea(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'restaurant_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'restaurant-search',
                'placeholder': 'Search for a restaurant...',
                'autocomplete': 'off'
            }),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
 
class LookupWineForm(forms.Form):
    """
    Form for searching wines using various filters.

    Fields:
    - winery: Winery name search field.
    - varietal: Grape varietal search field.
    - min_price: Minimum price filter.
    - max_price: Maximum price filter.
    - min_rating: Minimum rating filter.
    - max_rating: Maximum rating filter.
    """
    winery = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    varietal = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    min_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    min_rating = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_rating = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
