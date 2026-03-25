from ..models import Song, Album

def create_song(data, files, album):
    raw_tags = data.get('tags', '')
    #separate tags
    tags = ",".join([t.strip().lower() for t in raw_tags.split(",") if t.strip()])
    #return the song object with all data
    return Song.objects.create(
        title=data.get('title'),
        artist=data.get('artist'),
        tags=tags,
        audio_file=files.get('audio_file'),
        album=album,
    )
    