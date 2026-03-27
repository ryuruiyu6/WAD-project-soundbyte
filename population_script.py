import os
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD_project_soundbyte.settings')

import django

django.setup()

from django.contrib.auth.models import User
from django.core.files import File
from soundbytes.models import (
    Album,
    Comment,
    Download,
    Follow,
    Genre,
    Like,
    Playlist,
    Post,
    Profile,
    ProfileView,
    Song,
)


BASE_DIR = Path(__file__).resolve().parent

AUDIO_CANDIDATE_GROUPS = {
    'midnight_pulse': [
        BASE_DIR / 'sample_data/audio/no_more_no_more.mp3',
        Path('/Users/zakharov/Downloads/media/songs/no_more_no_more.mp3'),
    ],
    'neon_streets': [
        BASE_DIR / 'sample_data/audio/opening_shot.mp3',
        Path('/Users/zakharov/Downloads/media/songs/GJ2025_Opening_Shot.mp3'),
    ],
    'soft_horizon': [
        BASE_DIR / 'sample_data/audio/gossip.mp3',
        Path('/Users/zakharov/Downloads/media/songs/06_Gossip.mp3'),
    ],
    'glass_signals': [
        BASE_DIR / 'sample_data/audio/no_more_no_more.mp3',
        Path('/Users/zakharov/Downloads/media/songs/no_more_no_more.mp3'),
    ],
}

COVER_CANDIDATES = [
    BASE_DIR / 'sample_data/images/wall.png',
    BASE_DIR / 'media/covers/Dancing_lasha_tumbai_cover.jpg',
    BASE_DIR / 'media/covers/soundbyte_logo.png',
    BASE_DIR / 'static/soundbyte_logo.png',
    Path('/Users/zakharov/Downloads/media/covers/wall.png'),
]


def first_existing(paths):
    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError(f'None of these files exist: {paths}')


COVER_PATH = first_existing(COVER_CANDIDATES)


def get_or_make_user(username, password, email):
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email},
    )
    if created or not user.check_password(password):
        user.email = email
        user.set_password(password)
        user.save()
    return user


def get_or_make_profile(user, user_type, artist_name='', bio=''):
    profile, _ = Profile.objects.get_or_create(
        user=user,
        defaults={
            'user_type': user_type,
            'artist_name': artist_name,
            'bio': bio,
        },
    )
    profile.user_type = user_type
    profile.artist_name = artist_name
    profile.bio = bio
    profile.is_verified_artist = user_type == 'ARTIST'
    profile.save()
    return profile


def get_or_make_album(title, artist):
    album = Album.objects.filter(title=title, artist=artist).first()
    if album:
        return album
    album = Album(title=title, artist=artist)
    with COVER_PATH.open('rb') as cover_file:
        album.cover_image.save(COVER_PATH.name, File(cover_file), save=True)
    return album


def get_or_make_song(title, artist, album, tags, genres, audio_paths):
    song = Song.objects.filter(title=title, artist=artist, album=album).first()
    if not song:
        song = Song(title=title, artist=artist, album=album, tags=tags)
        audio_path = first_existing(audio_paths)
        with audio_path.open('rb') as audio_file:
            song.audio_file.save(audio_path.name, File(audio_file), save=True)
    song.genres.set(genres)
    return song


def ensure_follow(follower, following):
    if follower == following:
        return
    follow, created = Follow.objects.get_or_create(follower=follower, following=following)
    if created:
        following.profile.followers.add(follower)
    return follow


def ensure_like(user, song):
    like, created = Like.objects.get_or_create(user=user, song=song)
    if created:
        song.like_count += 1
        song.save(update_fields=['like_count'])
    return like


def ensure_comment(user, song, body):
    return Comment.objects.get_or_create(user=user, song=song, body=body)


def ensure_download(user, song, times=1):
    existing = Download.objects.filter(user=user, song=song).count()
    missing = max(0, times - existing)
    for _ in range(missing):
        Download.objects.create(user=user, song=song)
        song.download_count += 1
    if missing:
        song.save(update_fields=['download_count'])


def ensure_profile_view(viewer, profile_user, times=1):
    existing = ProfileView.objects.filter(viewer=viewer, profile_user=profile_user).count()
    missing = max(0, times - existing)
    for _ in range(missing):
        ProfileView.objects.create(viewer=viewer, profile_user=profile_user)
    if missing:
        profile = profile_user.profile
        profile.profile_views = ProfileView.objects.filter(profile_user=profile_user).count()
        profile.save(update_fields=['profile_views'])


def ensure_playlist(user, title, songs):
    playlist, _ = Playlist.objects.get_or_create(user=user, title=title)
    playlist.songs.set(songs)
    return playlist


def main():
    print(f'Using cover file: {COVER_PATH}')
    print('Using sample audio files:')
    for label, paths in AUDIO_CANDIDATE_GROUPS.items():
        print(f'  {label}: {first_existing(paths)}')

    artist1 = get_or_make_user('artist1', 'pass1234', 'artist1@example.com')
    artist2 = get_or_make_user('artist2', 'pass1234', 'artist2@example.com')
    fan1 = get_or_make_user('fan1', 'pass1234', 'fan1@example.com')
    fan2 = get_or_make_user('fan2', 'pass1234', 'fan2@example.com')

    get_or_make_profile(artist1, 'ARTIST', 'Illia Beats', 'Electronic artist and producer.')
    get_or_make_profile(artist2, 'ARTIST', 'Rui Waves', 'Indie pop artist.')
    get_or_make_profile(fan1, 'LISTENER', '', 'Testing listener account.')
    get_or_make_profile(fan2, 'LISTENER', '', 'Second listener account.')

    rock, _ = Genre.objects.get_or_create(name='Rock')
    pop, _ = Genre.objects.get_or_create(name='Pop')
    electronic, _ = Genre.objects.get_or_create(name='Electronic')
    indie, _ = Genre.objects.get_or_create(name='Indie')

    album1 = get_or_make_album('Illia Debut', 'artist1')
    album2 = get_or_make_album('Rui Sessions', 'artist2')

    song1 = get_or_make_song(
        'Midnight Pulse', 'artist1', album1, 'synth,night,drive',
        [electronic, pop], AUDIO_CANDIDATE_GROUPS['midnight_pulse']
    )
    song2 = get_or_make_song(
        'Neon Streets', 'artist1', album1, 'city,beat,late',
        [electronic, rock], AUDIO_CANDIDATE_GROUPS['neon_streets']
    )
    song3 = get_or_make_song(
        'Soft Horizon', 'artist2', album2, 'calm,indie,dream',
        [indie, pop], AUDIO_CANDIDATE_GROUPS['soft_horizon']
    )
    song4 = get_or_make_song(
        'Glass Signals', 'artist2', album2, 'alt,warm,vocal',
        [indie, electronic], AUDIO_CANDIDATE_GROUPS['glass_signals']
    )

    for song, views in [(song1, 12), (song2, 8), (song3, 15), (song4, 6)]:
        if song.view_count < views:
            song.view_count = views
            song.save(update_fields=['view_count'])

    ensure_follow(fan1, artist1)
    ensure_follow(fan1, artist2)
    ensure_follow(fan2, artist1)
    ensure_follow(artist2, artist1)

    ensure_like(fan1, song1)
    ensure_like(fan1, song3)
    ensure_like(fan2, song1)
    ensure_like(artist2, song1)
    ensure_like(artist1, song3)

    ensure_comment(fan1, song1, 'This track is great.')
    ensure_comment(fan1, song3, 'Love the vibe on this one.')
    ensure_comment(fan2, song2, 'This one should be on the home page.')
    ensure_comment(artist2, song1, 'Nice production.')
    ensure_comment(artist1, song3, 'Really clean sound.')

    ensure_download(fan1, song1, times=2)
    ensure_download(fan1, song3, times=1)
    ensure_download(fan2, song2, times=1)
    ensure_download(artist2, song1, times=1)

    ensure_profile_view(fan1, artist1, times=2)
    ensure_profile_view(fan1, artist2, times=1)
    ensure_profile_view(fan2, artist1, times=1)
    ensure_profile_view(artist2, artist1, times=1)

    ensure_playlist(fan1, 'Late Night Rotation', [song1, song2, song3])
    ensure_playlist(fan1, 'Eurovision Energy', [song1, song4])
    ensure_playlist(fan2, 'Testing Playlist', [song2, song3, song4])

    Post.objects.get_or_create(text_content='New release this week from Illia Beats.')
    Post.objects.get_or_create(text_content='Studio session clips coming soon.')

    print('\nSeed complete.')
    print('Login accounts:')
    print('  artist1 / pass1234')
    print('  artist2 / pass1234')
    print('  fan1    / pass1234')
    print('  fan2    / pass1234')
    print('\nSongs:')
    for song in Song.objects.order_by('artist', 'title'):
        print(
            f'  {song.id}: {song.title} by {song.artist} | '
            f'views={song.view_count} downloads={song.download_count} likes={song.like_count}'
        )


if __name__ == '__main__':
    main()
