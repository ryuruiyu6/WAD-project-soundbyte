import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD_project_soundbyte.settings')
import django
django.setup()

from django.contrib.auth.models import User
from soundbytes.models import Genre, Album, Song

# Create test user
user, created = User.objects.get_or_create(username='testuser')
if created:
    user.set_password('testpass123')
    user.save()

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