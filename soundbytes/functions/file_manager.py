from ..models import Song

def create_song(data, files):
    return Song.objects.create(
        title=data.get('title'),
        artist=data.get('artist'),
        genre=data.get('genre'),
        tags=data.get('tags'),
        audio_file=files.get('audio_file'),
        cover_image=files.get('cover_image')
    )