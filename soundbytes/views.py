from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from .functions.file_manager import create_song
from .functions.search_function import search, sort_songs
from .forms import UserForm,ProfileForm
from .models import Song, Genre, Album

def landing(request):

    context_dict={}
    context_dict['boldmessage']='hi'

    response = render(request, 'soundbytes/landing.html', context = context_dict)
    return response

def signup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request,
                  'soundbytes/signup.html',
                  context = {'user_form':user_form,
                             'profile_form':profile_form,
                             'registered':registered})

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect(reverse('soundbytes:home'))
            else:
                return HttpResponse("Your Soundbytes account is diabled")
        else:
            return HttpResponse("Invalid sign-in details.")
    else:
        return render(request,'soundbytes/signin.html')
    
#Auth only below
    
@login_required
def signout(request):
    logout(request)
    return redirect(reverse('rango:index'))

@login_required
def home(request):
    return render(request,'soundbytes_auth/home.html')

@login_required
def profile(request):
    return render(request,'soundbytes_auth/profile.html')


@csrf_exempt
def upload_song(request):
    #must have album
    if request.method == 'POST':
        album_id = request.POST.get('album')
        if not album_id:
            #if no album return error to prevent crash
            return JsonResponse({'error': 'You must select an album'})
        album = Album.objects.get(id=album_id)
        #create song!!
        song = create_song(request.POST, request.FILES, album)
        #assign genres and add
        genre_ids = request.POST.getlist('genres')
        song.genres.set(genre_ids)
        return redirect('/search-page/')
    return JsonResponse({'error': 'Invalid request'})

@csrf_exempt
def search_songs(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '')
    #return songs that meet the search criteria
    songs = search(query)
    songs = sort_songs(songs, sort_by)
    return JsonResponse(list(songs.values()), safe=False)

def upload_page(request):
    genres = Genre.objects.all()
    albums = Album.objects.all()
    return render(request, 'soundbytes_auth/upload.html', {'genres': genres, 'albums': albums})

def search_page(request):
    query = request.GET.get('q', '')
    genre = request.GET.get('genre')
    songs = search(query)
    #filter by genre
    if genre:
        songs = songs.filter(genres__name=genre)
    genres = Genre.objects.all()
    sort_by = request.GET.get('sort', '')
    songs = sort_songs(songs, sort_by)
    return render(request, 'soundbytes_auth/search.html', {'songs': songs, 'genres': genres})

def stream_song(request, song_id):
    song = Song.objects.get(id=song_id)
    #increase view count on stream
    song.view_count += 1
    song.save()
    #play song
    return FileResponse(song.audio_file.open(), content_type='audio/mpeg')

def create_album(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        artist = request.POST.get('artist')
        cover = request.FILES.get('cover_image')
        #create album with data above got from page
        Album.objects.create(
            title=title,
            artist=artist,
            cover_image=cover
        )
        return redirect('/upload-page/')
    return render(request, 'soundbytes_auth/create_album.html')

def album_page(request, album_id):
    #displays songs in that album
    album = Album.objects.get(id=album_id)
    songs = Song.objects.filter(album=album)
    return render(request, 'soundbytes_auth/album.html', {'album': album,'songs': songs})

def trending_page(request):
    songs = Song.objects.all()
    for song in songs:
        #assigns each song a value based on likes, views and
        #downloads to calculate how popular it is
        song.score = (
            song.like_count * 3 +
            song.view_count * 2 +
            song.download_count * 4
        )
    #displays top 10 songs
    songs = sorted(songs, key=lambda x: x.score, reverse=True)[:10]
    return render(request, 'soundbytes_auth/trending.html', {'songs': songs})