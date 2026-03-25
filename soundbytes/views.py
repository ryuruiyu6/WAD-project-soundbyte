from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse
from .functions.file_manager import create_song
from .functions.search_function import search, sort_songs
from django.views.decorators.csrf import csrf_exempt
from .models import Song, Genre, Album, Post

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
    sort_by = request.GET.get('sort', '')
    content_type = request.GET.get('type', 'all')
    genres = Genre.objects.all()
    #songs
    songs = search(query)
    if genre:
        songs = songs.filter(genres__name=genre)
    #posts
    posts = Post.objects.all()
    if query:
        posts = posts.filter(text_content__icontains=query)
    #all sort (automatically sorts by newest)
    if not sort_by or sort_by == 'new':
        songs = songs.order_by('-upload_date')
        posts = posts.order_by('-created_at')
        songs = list(songs)
        posts = list(posts)
        results = []
        if content_type == 'songs':
            results = [{'type': 'song', 'data': s} for s in songs]
        elif content_type == 'posts':
            results = [{'type': 'post', 'data': p} for p in posts]
        else:
            #mix posts and songs
            max_len = max(len(songs), len(posts))
            for i in range(max_len):
                if i < len(songs):
                    results.append({'type': 'song', 'data': songs[i]})
                if i < len(posts):
                    results.append({'type': 'post', 'data': posts[i]})
    #sort by likes
    elif sort_by == 'likes':
        songs = list(songs.order_by('-like_count'))
        posts = list(posts.order_by('-like_count'))
        results = []
        #{comment here}
        if content_type == 'songs':
            results = [{'type': 'song', 'data': s} for s in songs]
        elif content_type == 'posts':
            results = [{'type': 'post', 'data': p} for p in posts]
        else:
            #{comment here}
            max_len = max(len(songs), len(posts))
            for i in range(max_len):
                if i < len(songs):
                    results.append({'type': 'song', 'data': songs[i]})
                if i < len(posts):
                    results.append({'type': 'post', 'data': posts[i]})
    #sort by views
    elif sort_by == 'views':
        songs = songs.order_by('-view_count')
        results = [{'type': 'song', 'data': s} for s in songs]
    #sort by downloads
    elif sort_by == 'downloads':
        songs = songs.order_by('-download_count')
        results = [{'type': 'song', 'data': s} for s in songs]
    else:
        results = []
    return render(request, 'soundbytes_auth/search.html', {'results': results, 'genres': genres})

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
    results = []
    # song scores
    songs = Song.objects.all()
    for song in songs:
        score = ((song.like_count * 3) + (song.view_count * 2) + (song.download_count * 4))
        results.append({'type': 'song', 'data': song, 'score': score})
    # score posts
    posts = Post.objects.all()
    for post in posts:
        score = post.like_count * 5
        results.append({'type': 'post', 'data': post, 'score': score})
    # find top ten
    results = sorted(results, key=lambda x: x['score'], reverse=True)[:10]
    return render(request, 'soundbytes_auth/trending.html', {'results': results})

def upload(request):
    print("UPLOAD ROUTER HIT")
    if request.method == 'POST':
        content_type = request.POST.get('content_type')
        if content_type == 'song':
            return upload_song(request)
        elif content_type == 'post':
            return upload_post(request)
        else:
            return JsonResponse({'error': f'Invalid content type: {content_type}'})
    return JsonResponse({'error': 'Invalid request'})

def upload_post(request):
    text = request.POST.get('text_content')
    image = request.FILES.get('image_file')
    if not text and not image:
        return JsonResponse({'error': 'Post must contain text or an image'})
    Post.objects.create(text_content=text, image=image)
    return redirect('/search-page/')