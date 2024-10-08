from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Team(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    facebook_link = models.CharField(max_length=100)
    twitter_link = models.CharField(max_length=100)
    google_plus_link = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
    description = RichTextField(null=True)

    def __str__(self):
        return self.first_name
