from django.db.models import Q
from ..models import Song

def search(query):
    songs = Song.objects.all()
    if query:
        words = query.split()
        query_filter = Q()
        for word in words:
            #checks if the string in the search bar
            #is in either the title, artist, genre or a tag
            #all words in the search bar must be present to appear
            #eg rock bagpipes would only return things with rock and bagpipes
            #in it, not anything with rock OR bagpipes
            query_filter &= (
                Q(title__icontains=word) |
                Q(artist__icontains=word) |
                Q(genres__name__icontains=word) |
                Q(tags__icontains=word)
            )
        #only stores songs that meet the criteria
        songs = songs.filter(query_filter)
    return songs.distinct()

#    return Song.objects.filter(
#        Q(title__icontains=query) |
#        Q(artist__icontains=query) |
#        Q(genres__name__icontains=query) |
#        Q(tags__icontains=query)
#    ).distinct()

#sorting songs below
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