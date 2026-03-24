from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse
from .functions.file_manager import create_song
from .functions.search_function import search, sort_songs
from django.views.decorators.csrf import csrf_exempt
from .models import Song, Genre

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
    song = Song.objects.get(id=song_id)
    song.view_count += 1
    song.save()
    return FileResponse(song.audio_file.open(), content_type='audio/mpeg')
