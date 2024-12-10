from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    Represents a user profile.

    Fields:
    - user: One-to-one relationship with Django's User model.
    - first_name: User's first name.
    - last_name: User's last name.
    - email: User's email address.
    - city: City where the user is located (optional).
    - image_url: URL to the user's profile image (optional).
    - created_at: Timestamp when the profile was created.

    Methods:
    - get_wine_reviews: Retrieves all wine reviews associated with the user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    city = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_wine_reviews(self):
        return Review.objects.filter(user=self.user).order_by('-created_at')

class Wine(models.Model):
    """
    Represents a wine with its corresponding details.

    Fields:
    - name: Wine's name.
    - winery: Name of the winery producing the wine (optional).
    - category: Type of wine (e.g., Red, White) (optional).
    - varietal: Grape varietal used (optional).
    - appellation: Wine's geographic origin (optional).
    - alcohol: Alcohol content as a float (optional).
    - price: Wine's price as a decimal (optional).
    - rating: Wine's rating as an integer (optional).
    - reviewer: Name of the reviewer (optional).
    - review: Text review of the wine (optional).
    - country_of_origin: Country where the wine is produced (optional).

    Methods:
    - __str__: Returns the wine's name.
    """
    name = models.CharField(max_length=200, default="Wine Name")
    winery = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    varietal = models.CharField(max_length=100, blank=True, null=True)
    appellation = models.CharField(max_length=200, blank=True, null=True)
    alcohol = models.FloatField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rating = models.PositiveSmallIntegerField(blank=True, null=True)
    reviewer = models.CharField(max_length=100, blank=True, null=True)
    review = models.TextField(blank=True, null=True)
    country_of_origin = CountryField(blank_label="(Select country)", blank=True, null=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    """
    Represents a wine review.

    Fields:
    - user: The user who wrote the review.
    - wine: The wine being reviewed.
    - review_text: Text content of the review.
    - image_url: URL to an image of the wine or tasting experience (optional).
    - created_at: Timestamp when the review was created.
    - varietal: Grape varietal used (optional).
    - price: Price paid for the wine (optional).
    - rating: Overall rating of the wine out of 10.
    - body_rating: Body attribute rating out of 10.
    - finish_rating: Finish attribute rating out of 10.
    - taste_rating: Taste attribute rating out of 10.
    - country_of_origin: Country where the wine originates (optional).
    - restaurant_name: Name of the restaurant where the wine was tasted (optional).
    - latitude: Restaurant's latitude (optional).
    - longitude: Restaurant's longitude (optional).

    Methods:
    - __str__: Returns a string with the user's username and the wine's name.
    - location: Returns the restaurant's name if available, otherwise None.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wine = models.ForeignKey(Wine, on_delete=models.CASCADE, related_name="reviews", null=True, blank=True)
    review_text = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    varietal = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rating = models.IntegerField(default=5)
    body_rating = models.IntegerField(default=5)
    finish_rating = models.IntegerField(default=5)
    taste_rating = models.IntegerField(default=5)
    country_of_origin = CountryField(blank_label="(Select country)", blank=True, null=True)
    restaurant_name = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)


    def __str__(self):
        return f"{self.user.username}'s review of {self.wine.name}"
    
    def location(self):
        """
        If restaurant_name string contains a comma, only the first part(restaurant name) is returned.
        Otherwise, returns None.
        """
        if self.restaurant_name:
            return self.restaurant_name.split(',')[0]
        return None

    
class LookupWine(models.Model):
    """
    Represents wines available for recommendation from the winedata.csv data.

    Fields:
    - wine: wine name.
    - winery: Name of the winery (optional).
    - category: Type of wine (optional).
    - varietal: Grape varietal used (optional).
    - appellation: Geographic origin (optional).
    - alcohol: Alcohol content as a float (optional).
    - price: Price of the wine (optional).
    - rating: Rating given to the wine (optional).
    - reviewer: Name of the reviewer (optional).
    - review: Full text review (optional).

    Methods:
    - __str__: Returns the wine's name.
    """
    wine = models.CharField(max_length=255)  # Full wine name
    winery = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    varietal = models.CharField(max_length=255, blank=True, null=True)
    appellation = models.CharField(max_length=255, blank=True, null=True)
    alcohol = models.FloatField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rating = models.PositiveSmallIntegerField(blank=True, null=True)
    reviewer = models.CharField(max_length=255, blank=True, null=True)
    review = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.wine
    
class Favorite(models.Model):
    """
    Represents a user's favorited wine.

    Fields:
    - user: The user who favorited the wine.
    - wine: The wine that was favorited.
    - created_at: Timestamp when the wine was favorited.

    Meta:
    - unique_together: Makes sure that each wine can be favorited only once per user.

    Methods:
    - __str__: Returns a string with the user's username and the wine's name.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wine = models.ForeignKey(Wine, related_name="favorited_by", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'wine')

    def __str__(self):
        return f"{self.user.username} favorited {self.wine.name}"