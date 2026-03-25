from ..models import Song

def create_song(data, files):
    raw_tags = data.get('tags', '')
    #separate tags
    tags = ",".join([t.strip().lower() for t in raw_tags.split(",") if t.strip()])
    return Song.objects.create(
        title=data.get('title'),
        artist=data.get('artist'),
        tags=tags,
        audio_file=files.get('audio_file'),
        cover_image=files.get('cover_image')
    )
    