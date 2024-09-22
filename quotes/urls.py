## quotes/urls.py
## description: the app-specific URLs for the hw application

from django.urls import path        #path function to assosiate string to url 
from django.conf import settings    #import settings from django.conf
from . import views                 #import views from current directory

# create list of URLs for this app
urlpatterns = [
    path(r'', views.quotes, name="quotes"),
   ###path(r'quote', views.quote, name="quote"),
    path(r'show_all', views.show_all, name="show_all"),
    path(r'about', views.about, name="about"),
]