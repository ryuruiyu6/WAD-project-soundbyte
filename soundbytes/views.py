from django.shortcuts import render
from django.http import JsonResponse
from .functions.file_manager import create_song
from .functions.search_function import search, sort_songs
from django.views.decorators.csrf import csrf_exempt

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
