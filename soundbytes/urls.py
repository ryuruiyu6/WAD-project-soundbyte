from django.urls import path
from soundbytes import views

app_name = 'soundbytes'

#all urls i used, please do not remove anything from this list!!
urlpatterns = [
    path('', views.landing, name='landing'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('signout/', views.signout, name='signout'),
    path('upload/', views.upload, name='upload'),
    path('search/', views.search_songs, name='search_songs'),
    path('upload-page/', views.upload_page, name='upload'),
    path('search-page/', views.search_page, name='search_page'),
    path('stream/<int:song_id>/', views.stream_song, name='stream_song'),
    path('create-album/', views.create_album, name='create_album'),
    path('album/<int:album_id>/', views.album_page, name='album_page'),
    path('trending/', views.trending_page, name='trending'),
    path('top/', views.top_page, name='top'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('playlists/<str:username>/', views.playlists, name='playlists'),
    #path('playlists/<str:username>/<str:playlist_title>/', views.profile, name='playlist'),
    #path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    #path('profile/edit/', views.profile_edit, name='profile_edit'),
    #path('analytics/<str:username>/', views.analytics, name='analytics'),
]