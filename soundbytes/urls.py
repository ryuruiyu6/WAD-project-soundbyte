from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_song),
    path('search/', views.search_songs),
    path('upload-page/', views.upload_page),
    path('search-page/', views.search_page),
    path('stream/<int:song_id>/', views.stream_song),
    path('create-album/', views.create_album),
    path('album/<int:album_id>/', views.album_page, name='album_page'),
    path('stream/<int:song_id>/', views.stream_song, name='stream_song'),
    path('trending/', views.trending_page, name='trending'),
] 