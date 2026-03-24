from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from .functions.file_manager import create_song
from .functions.search_function import search, sort_songs
from django.views.decorators.csrf import csrf_exempt
from .models import Song

@csrf_exempt
def upload_song(request):
    if request.method == 'POST':
        song = create_song(request.POST, request.FILES)
        return JsonResponse({'status': 'success', 'song_id': song.id})
    return JsonResponse({'error': 'Invalid request'})

@csrf_exempt
def search_songs(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '')
    songs = search(query)
    songs = sort_songs(songs, sort_by)
    return JsonResponse(list(songs.values()), safe=False)

def upload_page(request):
    return render(request, 'soundbytes_auth/upload.html')

def search_page(request):
    query = request.GET.get('q', '')
    genre = request.GET.get('genre')
    songs = search(query)
    if genre:
        songs = songs.filter(genre=genre)
    return render(request, 'soundbytes_auth/search.html', {'songs': songs})

def stream_song(request, song_id):
    song = Song.objects.get(id=song_id)
    song.view_count += 1
    song.save()
    return FileResponse(song.audio_file.open(), content_type='audio/mpeg')
