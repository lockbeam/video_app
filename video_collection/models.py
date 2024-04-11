from urllib import parse
from django.db import models
from django.core.exceptions import ValidationError

# urllib can parrse pieces of a url and extract speccific parts which we'll use for the video id

class Video(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    notes = models.TextField(blank=True, null=True) # value can be blank or null
    video_id = models.CharField(max_length=40, unique=True) # cannot add the same video twice

    # below parses the url provided for the id code before saving the video to the database
    def save(self, *args, **kwargs):

        # first check we have a youtube video
        if not self.url.startswith('https://www.youtube.com/watch'):
            raise ValidationError(f'Not a YouTube URL {self.url}')

        url_components = parse.urlparse(self.url)
        query_string = url_components.query
        if not query_string:
            raise ValidationError(f'Invalid YouTube URL {self.url}')
        parameters = parse.parse_qs(query_string, strict_parsing=True) #parses the id to the id number and then pairs them as a dictionary instead of a string
        v_parameters_list = parameters.get('v') # will return None if no key found - looking for a key of 'v'
        if not v_parameters_list: # checking if None or empty list
            raise ValidationError(f'Invalid YouTube URL, missing parameters {self.url}')
        self.video_id = v_parameters_list[0] #true if not None and at least one entry so continue towards parsing and saving the value pair

        super().save(*args, **kwargs) #return to django save model and save to database



    def __str__(self):
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url}, Video ID: {self.video_id}, Notes: {self.notes[:200]}' #truncate tp 200 char.