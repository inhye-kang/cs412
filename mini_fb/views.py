## mini_fb/views.py
# description: the logic to handle URL requests
from django.shortcuts import render
from . models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.shortcuts import redirect
from . forms import *
import random
from django.utils import timezone
from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User ## NEW
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth import login, authenticate



class ShowAllView(ListView):
    '''Create a subclass of ListView to display all profiles.'''
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        return context
    
class ShowProfileView(DetailView):
    '''Show the details for one profile.'''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'
    
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
        context = self.get_context_data()
        user_form = context['user_form']

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
        context['current_time'] = timezone.now()
        return context
    
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''Create new status message'''
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_success_url(self) -> str:
        return reverse('profile', kwargs={'pk': self.object.profile.pk})

    def form_valid(self, form):
        sm = form.save(commit=False)
        
        sm.profile = self.profile
        sm.save()

        files = self.request.FILES.getlist('files')
        for file in files:
            image = Image(status_message=sm, image_file=file)
            image.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        context['current_time'] = timezone.now()
        return context
    
    def dispatch(self, request, *args, **kwargs):
        self.profile = Profile.objects.filter(user=request.user).first()
        return super().dispatch(request, *args, **kwargs)
    
    def get_login_url(self) -> str:
        '''Return the URL to the login page.'''
        return reverse('login')

    
""" class CreateCommentView(CreateView):
    form_class = CreateCommentForm
    template_name = "create_comment_form.html"

    def get_success_url(self) -> str:
        return reverse("show_all") """
    
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
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the existing context
        context = super().get_context_data(**kwargs)
        # Add 'current_time' to the context
        context['current_time'] = timezone.now()
        context['profile'] = self.object
        return context
    
    def get_login_url(self) -> str:
        '''Return the URL to the login page.'''
        return reverse('login')
    
    def get_object(self):
        return Profile.objects.filter(user=self.request.user).first()
    
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        profile = self.object.profile
        return reverse('profile', kwargs={'pk': profile.pk})
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # Call the base implementation first to get the existing context
        context = super().get_context_data(**kwargs)
        # Add 'current_time' to the context
        context['current_time'] = timezone.now()
        profile = self.object.profile
        context['profile'] = profile

        return context
    
    def get_login_url(self) -> str:
        '''Return the URL to the login page.'''
        return reverse('login')
    
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'

    def get_success_url(self):
        profile = self.object.profile
        return reverse('profile', kwargs={'pk': profile.pk})
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the existing context
        context = super().get_context_data(**kwargs)
        # Add 'current_time' to the context
        context['current_time'] = timezone.now()
        context['status_message'] = self.object
        return context
    
    def get_login_url(self) -> str:
        '''Return the URL to the login page.'''
        return reverse('login')
    
class CreateFriendView(LoginRequiredMixin, CreateView):
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        other_pk = kwargs.get('other_pk')
        
        try:
            profile = Profile.objects.filter(user=request.user).first()
            other_profile = Profile.objects.get(pk=other_pk)
            
            if profile != other_profile:
                profile.add_friend(other_profile)

        except Profile.DoesNotExist:
            pass
        
        return redirect('profile', pk=pk)
    
    def get_login_url(self) -> str:
        '''Return the URL to the login page.'''
        return reverse('login')

class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        context['friend_suggestions'] = profile.get_friend_suggestions()
        context['current_time'] = timezone.now()

        return context
    
    def get_object(self):
        return Profile.objects.filter(user=self.request.user).first()
    
class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        context['news_feed'] = profile.get_news_feed()
        context['current_time'] = timezone.now()
        return context