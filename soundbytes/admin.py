from django.contrib import admin
from .models import Song, Genre

admin.site.register(Song)
admin.site.register(Genre)