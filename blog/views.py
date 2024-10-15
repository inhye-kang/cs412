## mini_fb/views.py
# description: the logic to handle URL requests
#from django.shortcuts import render
from .models import Profile
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from .forms import CreateProfileForm, CreateStatusMessageForm
import random
from django.utils import timezone
from typing import Any, Dict

class ShowAllView(ListView):
    '''Create a subclass of ListView to display all profiles.'''
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        return context
    
class CreateProfileView(CreateView):
    '''create new profile'''
    form_class = CreateProfileForm

    template_name = 'mini_fb/create_profile_form.html' ## reusing same template!!
    
    def get_success_url(self) -> str:
        return reverse('profile', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        return context
    
class CreateStatusMessageView(CreateView):
    '''create new status message'''
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'
    
    def get_success_url(self) -> str:
        return reverse('profile', kwargs={'pk': self.object.profile.pk})
    
    def form_valid(self, form):
        print(form.cleaned_data)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = Profile.objects.get(pk=pk)
        context['current_time'] = timezone.now()
        return context
    
class CreateCommentView(CreateView):
    form_class = CreateCommentForm
    template_name = "create_comment_form.html"

    def get_success_url(self) -> str:
        return reverse("show_all")
    
class ShowProfileView(DetailView):
    '''Show the details for one profile.'''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the existing context
        context = super().get_context_data(**kwargs)
        # Add 'current_time' to the context
        context['current_time'] = timezone.now()
        return context