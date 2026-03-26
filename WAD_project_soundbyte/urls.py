from django.urls import path, include
from soundbytes import views as soundbytes_views
from onboarding import views as onboarding_views

urlpatterns = [
    # Onboarding routes (landing pages)
    path('', onboarding_views.landing, name='landing'),
    path('register/', onboarding_views.register, name='register'),
    path('sign-in/', onboarding_views.sign_in, name='sign_in'),
    
    # Soundbytes authentication routes
    path('signup/', soundbytes_views.signup, name='signup'),
    path('signin/', soundbytes_views.signin, name='signin'),
    path('signout/', soundbytes_views.signout, name='signout'),
    
    # Main app routes
    path('home/', soundbytes_views.home, name='home'),
    path('profile/', soundbytes_views.profile, name='profile'),
    path('upload/', soundbytes_views.upload),
    path('search/', soundbytes_views.search_songs),
    path('upload-page/', soundbytes_views.upload_page),
    path('search-page/', soundbytes_views.search_page),
    path('stream/<int:song_id>/', soundbytes_views.stream_song, name='stream_song'),
    path('create-album/', soundbytes_views.create_album),
    path('album/<int:album_id>/', soundbytes_views.album_page, name='album_page'),
    path('trending/', soundbytes_views.trending_page, name='trending'),
]
