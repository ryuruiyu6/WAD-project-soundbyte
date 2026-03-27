from django.contrib import admin
from .models import Album, Comment, Download, Follow, Genre, Like, Post, ProfileView, Song

#for testing purposes can be removed later
admin.site.register(Song)
admin.site.register(Genre)
admin.site.register(Album)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Download)
admin.site.register(ProfileView)
