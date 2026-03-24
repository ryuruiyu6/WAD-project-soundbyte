from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_song),
    path('search/', views.search_songs),
    path('upload-page/', views.upload_page),
    path('search-page/', views.search_page),
    path('stream/<int:song_id>/', views.stream_song),
] 