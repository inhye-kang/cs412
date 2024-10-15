## mini_fb/urls.py
## description: the app-specific URLS for the mini_fb application

from django.urls import path
from .views import ShowAllView, ShowProfileView, CreateProfileView, CreateStatusMessageView # our view class definition 

urlpatterns = [
    # map the URL (empty string) to the view
    # path(url, view, name)
    path('', ShowAllView.as_view(), name='show_all_profiles'), 
    path('profile/<int:pk>', ShowProfileView.as_view(), name='profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name='create_status')
]