from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images',blank=True)
    slug = models.SlugField(unique=True)

    def save(self,*args,**kwargs):
        self.slug=slugify(self.user.username)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.user.username

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