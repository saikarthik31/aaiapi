from django.db import models
from django.contrib.auth.models import User


class SearchResult(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    content = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return str(self.title)


#second model for datble data


class Employee(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    department = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

# model for content_manager





class Content(models.Model): 
    VISIBILITY_CHOICES = [
        ('onlyme', 'Only Me'),
        ('subscribers', 'Subscribers'),
        ('public', 'Public'),
    ]
    
    CONTENT_TYPE_CHOICES = [
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('text', 'Text'),
        ('file', 'File'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='onlyme')
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True) 
    tags = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.title)
