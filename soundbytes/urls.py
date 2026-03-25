from django.urls import path
from soundbytes import views

app_name = 'soundbytes'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('signin/',views.signin,name='signin'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('creatordb/', views.creator_dashboard, name='creator_dashboard'),
    path('signout/', views.signout, name='signout'),
    path('upload/', views.upload_song, name='upload_song'),
    path('search/', views.search_songs, name='search'),
    path('upload-page/', views.upload_page, name='upload_page'),
    path('search-page/', views.search_page, name='search_page'),
    path('stream/<int:song_id>/', views.stream_song, name='stream_song'),
    path('download/<int:song_id>/', views.download_song, name='download_song'),
    path('like/<int:song_id>/', views.toggle_like, name='toggle_like'),
    path('comment/<int:song_id>/', views.add_comment, name='add_comment'),
    path('follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
] 
