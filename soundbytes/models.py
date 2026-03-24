from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Song(models.Model):
    #song data
    title = models.CharField(max_length = 50)
    artist = models.CharField(max_length = 50)
    genres = models.ManyToManyField(Genre)
    tags = models.TextField(max_length=50, blank = True)
    #files!!!
    audio_file = models.FileField(upload_to = 'songs/')
    cover_image = models.ImageField(upload_to = 'covers/', null = True, blank = True)
    #post data
    upload_date = models.DateTimeField(auto_now_add = True)
    download_count = models.IntegerField(default = 0)
    view_count = models.IntegerField(default = 0)
    like_count = models.IntegerField(default = 0)

    def __str__(self):
        return self.title