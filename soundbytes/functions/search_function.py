from django.db.models import Q
from ..models import Song

def search(query):
    songs = Song.objects.all()

    if query:
        words = query.split()

        query_filter = Q()

        for word in words:
            query_filter &= (
                Q(title__icontains=word) |
                Q(artist__icontains=word) |
                Q(genres__name__icontains=word) |
                Q(tags__icontains=word)
            )

        songs = songs.filter(query_filter)

    return songs.distinct()

#    return Song.objects.filter(
#        Q(title__icontains=query) |
#        Q(artist__icontains=query) |
#        Q(genres__name__icontains=query) |
#        Q(tags__icontains=query)
#    ).distinct()

def sort_songs(songs, sort_by):
    if sort_by == 'views':
        return songs.order_by('-view_count')
    elif sort_by == 'downloads':
        return songs.order_by('-download_count')
    elif sort_by == 'likes':
        return songs.order_by('-like_count')
    elif sort_by == 'new':
        return songs.order_by('-upload_date')
    return songs