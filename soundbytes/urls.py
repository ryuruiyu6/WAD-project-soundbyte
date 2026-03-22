from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_song),
    path('search/', views.search_songs),
]