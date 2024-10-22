# mini_fb/models.py
from django.db import models
class Profile(models.Model):
    '''Encapsulate the idea of a a profile of some user.'''
    # data attributes of a profile:
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    email = models.TextField(blank=False)
    city = models.TextField(blank=False)
    image_url = models.URLField(blank=True)
    
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
    
    def get_images(self):
        '''Return all images associated with this StatusMessage.'''
        return Image.objects.filter(status_message=self)

    
class Image(models.Model):
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE, related_name="images")
    image_file = models.ImageField(upload_to='status_images/')
    upload_ts = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image for status: {self.status_message.message} uploaded at {self.upload_ts}'