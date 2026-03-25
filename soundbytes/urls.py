from django.urls import path
from . import views

#all urls i used, please do not remove anything from this list!!
urlpatterns = [
    path('upload/', views.upload),
    path('search/', views.search_songs),
    path('upload-page/', views.upload_page),
    path('search-page/', views.search_page),
    path('stream/<int:song_id>/', views.stream_song),
    path('create-album/', views.create_album),
    path('album/<int:album_id>/', views.album_page, name='album_page'),
    path('stream/<int:song_id>/', views.stream_song, name='stream_song'),
    path('trending/', views.trending_page, name='trending'),
] 