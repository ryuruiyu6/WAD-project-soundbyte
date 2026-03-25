from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import FileResponse, HttpResponse, JsonResponse
from .functions.file_manager import create_song
from .functions.search_function import search, sort_songs
from django.views.decorators.csrf import csrf_exempt
from .forms import ProfileForm, UserForm
from .models import Song, Genre

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
                return redirect(reverse('soundbytes:landing'))
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
    return redirect(reverse('soundbytes:landing'))

def home(request):
    return render(request, 'soundbytes_auth/home.html')

def profile(request):
    return render(request, 'soundbytes_auth/profile.html')

@csrf_exempt
def upload_song(request):
    if request.method == 'POST':
        song = create_song(request.POST, request.FILES)
        genre_ids = request.POST.getlist('genres')
        song.genres.set(genre_ids)
        return redirect('/search-page/')
    return JsonResponse({'error': 'Invalid request'})

@csrf_exempt
def search_songs(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '')
    songs = search(query)
    songs = sort_songs(songs, sort_by)
    return JsonResponse(list(songs.values()), safe=False)

def upload_page(request):
    genres = Genre.objects.all()
    return render(request, 'soundbytes_auth/upload.html', {'genres': genres})

def search_page(request):
    query = request.GET.get('q', '')
    genre = request.GET.get('genre')
    songs = search(query)
    if genre:
        songs = songs.filter(genres__name=genre)
    genres = Genre.objects.all()
    sort_by = request.GET.get('sort', '')
    songs = sort_songs(songs, sort_by)
    return render(request, 'soundbytes_auth/search.html', {'songs': songs, 'genres': genres})

def stream_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    song.view_count += 1
    song.save()
    return FileResponse(song.audio_file.open(), content_type='audio/mpeg')
