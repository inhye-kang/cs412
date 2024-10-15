# blog/models.py
from django.db import models
class Profile(models.Model):
    '''Encapsulate the idea of a a profile of some user.'''
    # data attributes of a profile:
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    email = models.TextField(blank=False)
    city = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True) ## new
    
    def get_status_messages(self):
        '''Return status messages of Profile object.'''
        return StatusMessage.objects.filter(profile=self)

class StatusMessage(models.Model):
    '''Encapsulate the idea of a status message on an profile.'''
    
    # data attributes of a Comment:
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    message = models.TextField(blank=False)
    ts = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this status object.'''
        return f'{self.message}'