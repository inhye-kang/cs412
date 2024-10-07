## description: logic to handle URL requests

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random
from .models import Profile
from datetime import datetime, timedelta
from django.views.generic import ListView


class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['current_time'] = time.ctime()
        return context