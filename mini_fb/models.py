# mini_fb/models.py
from django.db import models
from django.contrib.auth.models import User

from django.db.models import Q

class Profile(models.Model):
    '''Encapsulate the idea of a a profile of some user.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # data attributes of a profile:
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    email = models.TextField(blank=False)
    city = models.TextField(blank=False)
    image_url = models.URLField(blank=True)
    
    def get_status_messages(self):
        '''Return status messages of Profile object.'''
        return StatusMessage.objects.filter(profile=self)
    
    def get_friends(self):
        '''Return all friends of this Profile.'''
        friend_instances = Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))

        friends = []
        for f in friend_instances:
            if f.profile1 == self:
                friends.append(f.profile2)
            else:
                friends.append(f.profile1)
        return friends
    
    def add_friend(self, other):
        if self == other:
            return 'Cannot add self as friend'

        friendship = Friend.objects.filter(
            models.Q(profile1=self, profile2=other) | 
            models.Q(profile1=other, profile2=self)
        ).exists()

        if friendship:
            return 'Friendship already exists'
        
        Friend.objects.create(profile1=self, profile2=other)
        return 'Friend added successfully'
    
    def get_friend_suggestions(self):
        '''Return a list of potential friends who are not currently friends with this Profile.'''
        current_friends = self.get_friends()
        
        suggestions = Profile.objects.exclude(id=self.id).exclude(id__in=[friend.id for friend in current_friends])
        
        return suggestions
    
    def get_news_feed(self):
        friends = self.get_friends()
        
        status_messages = StatusMessage.objects.filter(
            Q(profile=self) | Q(profile__in=friends)
        ).order_by('-ts')
        
        return status_messages

class StatusMessage(models.Model):
    '''Encapsulate the idea of a status message on an profile.'''
    
    # data attributes of a Comment:
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    message = models.TextField(blank=False)
    ts = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this status object.'''
        return f'{self.message}'
    
    def get_images(self):
        '''Return all images associated with this StatusMessage.'''
        return Image.objects.filter(status_message=self)

    
class Image(models.Model):
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE, related_name="images")
    image_file = models.ImageField(upload_to='status_images/')
    upload_ts = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image for status: {self.status_message.message} uploaded at {self.upload_ts}'
    
class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name = 'profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name = 'profile2')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile1} and {self.profile2} became friends at {self.timestamp}'