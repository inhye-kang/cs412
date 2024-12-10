from django.contrib import admin
from .models import Wine, Review, UserProfile, Favorite

admin.site.register(UserProfile)
admin.site.register(Wine)
admin.site.register(Review)
admin.site.register(Favorite)