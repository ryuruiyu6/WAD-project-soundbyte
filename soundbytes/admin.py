from django.contrib import admin
from .models import Comment, Download, Follow, Genre, Like, Profile, ProfileView, Song

admin.site.register(Song)
admin.site.register(Genre)
admin.site.register(Profile)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Download)
admin.site.register(ProfileView)
