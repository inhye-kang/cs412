## quotes/urls.py
## description: the app-specific URLs for the hw application

from django.urls import path        #path function to assosiate string to url 
from django.conf import settings    #import settings from django.conf
from . import views                 #import views from current directory

# create list of URLs for this app
urlpatterns = [
    path(r'', views.main, name="main"),
    path(r'order', views.order, name="order"),
    path(r'confirmation', views.confirmation, name="confirmation"),
]