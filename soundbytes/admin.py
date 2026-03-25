from django.contrib import admin
from .models import Song, Genre, Album, Post

#for testing purposes can be removed later
admin.site.register(Song)
admin.site.register(Genre)
admin.site.register(Album)
admin.site.register(Post)