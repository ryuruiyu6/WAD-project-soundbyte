from django.urls import path
from soundbytes import views

app_name = 'soundbytes'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('signin/',views.signin,name='signin'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('signout/', views.signout, name='signout'),
    path('upload/', views.upload_song),
    path('search/', views.search_songs),
]