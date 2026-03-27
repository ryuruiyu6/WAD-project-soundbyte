import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD_project_soundbyte.settings')
import django
django.setup()

from django.contrib.auth.models import User
from soundbytes.models import Genre, Album, Song, Profile

# Create test user
user, created = User.objects.get_or_create(username='testuser')
if created:
    user.set_password('testpass123')
    user.save()

for n in ['Alpha','Beta','Charlie','Delta','Echo','Foxtrot']:
    user, user_created = User.objects.get_or_create(username=n)
    if user_created:
        user.set_password('123')
        user.save()
        profile, prof_created = Profile.objects.update_or_create(user=user)
        if prof_created:
            profile.user_type='Artist'
            profile.bio=f'Hi this is {n}, I am an artist'
            profile.artist_name=f'{n} Doe'
            profile.save()
        

for n in ['Golf','Hotel','Indigo','Juliett','Kilo','Lima']:
    user, user_created = User.objects.get_or_create(username=n)
    if user_created:
        user.set_password('123')
        user.save()
        profile, prof_created = Profile.objects.update_or_create(user=user)
        if prof_created:
            profile.user_type='LISTENER'
            profile.bio=f'Hi this is {n}, I am a listener'
            profile.artist_name=f'{n} Doe'
            profile.save()
        

# Create genres
genres = ['Rock', 'Pop', 'Jazz', 'Hip Hop', 'Electronic']
for genre_name in genres:
    Genre.objects.get_or_create(name=genre_name)

# Create albums
album, created = Album.objects.get_or_create(
    title='Sample Album',
    artist='Test Artist'
)

print("Database populated successfully!")