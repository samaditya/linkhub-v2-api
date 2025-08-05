# profiles/models.py

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('cyberpunk', 'Cyberpunk'),
    ]

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, max_length=500)
    
    # Field for the custom URL slug
    slug = models.SlugField(unique=True, max_length=100)

    # Field for the background image upload
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    # Field for the theme selection
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='light')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.owner.username


class Link(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='links')
    title = models.CharField(max_length=100)
    url = models.URLField()

    # Field for the click count analytics
    click_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.title} | {self.url}'