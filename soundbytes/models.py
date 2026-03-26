from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import os
import datetime

def profile_picture_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"profile_{instance.user.username}_{instance.user.id}.{ext}"
    return os.path.join('profile_pictures', filename)

def banner_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"banner_{instance.user.username}_{instance.user.id}.{ext}"
    return os.path.join('banners', filename)

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('LISTENER', 'Music Listener'),
        ('ARTIST', 'Musician/Artist'),
        ('BOTH', 'Both Listener and Artist'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    slug = models.SlugField(unique=True)

    profile_picture = models.ImageField(
        upload_to=profile_picture_path,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])],
        blank=True, null=True)
    
    banner_image = models.ImageField(
        upload_to=banner_image_path,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        blank=True, null=True)
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='LISTENER')
    artist_name = models.CharField(max_length=100, blank=True, null=True)
    is_verified_artist = models.BooleanField(default=False)
    
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    
    date_joined_profile = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    
    is_public = models.BooleanField(default=True)
    show_activity = models.BooleanField(default=True)
    
    profile_views = models.PositiveIntegerField(default=0)
    total_likes_received = models.PositiveIntegerField(default=0)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.user.username)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ['-date_joined_profile']
    
    def get_display_name(self):
        return self.display_name if self.display_name else self.user.username
    
    def is_artist(self):
        return self.user_type in ['ARTIST', 'BOTH']
    
    def follower_count(self):
        return self.followers.count()
    
    def following_count(self):
        return self.user.following.count()

class Playlist(models.Model):
    title = models.CharField(max_length=255)
    songs = models.ManyToManyField('Song')

    def __str__(self):
        return self.title

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Album(models.Model):
    #album data
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='covers/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Song(models.Model):
    #song data
    title = models.CharField(max_length = 50)
    artist = models.CharField(max_length = 50)
    #genre can only be from premade genre list
    genres = models.ManyToManyField(Genre)
    #tags are optional dont need them (blank = true)
    tags = models.TextField(max_length=50, blank = True)
    #album must be an existing album in the database
    #there is a single album as a default if someone wants to
    #just realse one song
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    #files!!!
    audio_file = models.FileField(upload_to = 'songs/')
    #post data
    upload_date = models.DateTimeField(auto_now_add = True)
    download_count = models.IntegerField(default = 0)
    view_count = models.IntegerField(default = 0)
    like_count = models.IntegerField(default = 0)

    def __str__(self):
        return self.title