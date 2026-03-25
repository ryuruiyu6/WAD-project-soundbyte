from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

def profile_picture_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"profile_{instance.user.username}_{instance.user.id}.{ext}"
    return os.path.join('profile_pictures', filename)

def banner_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"banner_{instance.user.username}_{instance.user.id}.{ext}"
    return os.path.join('banners', filename)

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('LISTENER', 'Music Listener'),
        ('ARTIST', 'Musician/Artist'),
        ('BOTH', 'Both Listener and Artist'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    profile_picture = models.ImageField(
        upload_to=profile_picture_path,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])],
        blank=True, null=True
    )
    banner_image = models.ImageField(
        upload_to=banner_image_path,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        blank=True, null=True
    )
    
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
    
    class Meta:
        ordering = ['-date_joined_profile']
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_display_name(self):
        return self.display_name if self.display_name else self.user.username
    
    def is_artist(self):
        return self.user_type in ['ARTIST', 'BOTH']
    
    def follower_count(self):
        return self.followers.count()
    
    def following_count(self):
        return self.user.following.count()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()