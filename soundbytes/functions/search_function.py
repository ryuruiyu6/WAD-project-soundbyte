from django.db.models import Q
from ..models import Song

def search(query):
    return Song.objects.filter(
        Q(title__icontains=query) |
        Q(artist__icontains=query) |
        Q(genre__icontains=query) |
        Q(tags__icontains=query)
    )

def sort_songs(songs, sort_by):
    if sort_by == 'views':
        return songs.order_by('-view_count')
    elif sort_by == 'downloads':
        return songs.order_by('-download_count')
    elif sort_by == 'new':
        return songs.order_by('-upload_date')
    return songs