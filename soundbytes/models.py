from django.db import models

# Create your models here.

class Song(models.Model):
    title = models.CharField(max_length = 50)
    artist = models.CharField(max_length = 50)
    genre = models.CharField(max_length = 30)
    tags = models.TextField(blank = True)

    audio_file = models.FileField(upload_to = 'songs/')
    cover_image = models.ImageField(upload_to = 'covers/', null = True, blank = True)

    upload_date = models.DateTimeField(auto_now_add = True)

    download_count = models.IntegerField(default = 0)
    view_count = models.IntegerField(default = 0)
    like_count = models.IntegerField(default = 0)

    def __str__(self):
        return self.title