## quotes/urls.py
## description: the app-specific URLs for the hw application

from django.urls import path       
from django.conf import settings   
from . import views                
from .views import ShowAllProfilesView


urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
]