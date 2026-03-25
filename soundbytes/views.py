from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import FileResponse, HttpResponse, JsonResponse
from .functions.file_manager import create_song
from .functions.search_function import search, sort_songs
from django.views.decorators.csrf import csrf_exempt
from .forms import ProfileForm, UserForm
from .models import Comment, Download, Follow, Genre, Like, Profile, ProfileView, Song

def landing(request):

    context_dict={}
    context_dict['boldmessage']='hi'

    response = render(request, 'soundbytes/landing.html', context = context_dict)
    return response

def signup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request,
                  'soundbytes/signup.html',
                  context = {'user_form':user_form,
                             'profile_form':profile_form,
                             'registered':registered})

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect(reverse('soundbytes:landing'))
            else:
                return HttpResponse("Your Soundbytes account is diabled")
        else:
            return HttpResponse("Invalid sign-in details.")
    else:
        return render(request,'soundbytes/signin.html')
    
#Auth only below
    
@login_required
def signout(request):
    logout(request)
    return redirect(reverse('soundbytes:landing'))

def home(request):
    return render(request, 'soundbytes_auth/home.html')

def profile(request):
    username = request.GET.get('username')
    target_user = request.user if request.user.is_authenticated and not username else None

    if username:
        target_user = User.objects.filter(username=username).first()

    if target_user is None:
        return render(request, 'soundbytes_auth/profile.html', {'target_user': None})

    profile_obj = Profile.objects.filter(user=target_user).first()
    user_songs = Song.objects.filter(artist=target_user.username).order_by('-upload_date')

    if request.user.is_authenticated and request.user != target_user:
        ProfileView.objects.create(viewer=request.user, profile_user=target_user)

    follower_count = Follow.objects.filter(following=target_user).count()
    following_count = Follow.objects.filter(follower=target_user).count()
    profile_view_count = ProfileView.objects.filter(profile_user=target_user).count()
    is_following = False

    if request.user.is_authenticated and request.user != target_user:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=target_user
        ).exists()

    context = {
        'target_user': target_user,
        'profile_obj': profile_obj,
        'songs': user_songs,
        'follower_count': follower_count,
        'following_count': following_count,
        'profile_view_count': profile_view_count,
        'is_following': is_following,
    }
    return render(request, 'soundbytes_auth/profile.html', context)

@csrf_exempt
def upload_song(request):
    if request.method == 'POST':
        song = create_song(request.POST, request.FILES)
        genre_ids = request.POST.getlist('genres')
        song.genres.set(genre_ids)
        return redirect('/search-page/')
    return JsonResponse({'error': 'Invalid request'})

@csrf_exempt
def search_songs(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '')
    songs = search(query)
    songs = sort_songs(songs, sort_by)
    return JsonResponse(list(songs.values()), safe=False)

def upload_page(request):
    genres = Genre.objects.all()
    return render(request, 'soundbytes_auth/upload.html', {'genres': genres})

def search_page(request):
    query = request.GET.get('q', '')
    genre = request.GET.get('genre')
    songs = search(query)
    if genre:
        songs = songs.filter(genres__name=genre)
    genres = Genre.objects.all()
    sort_by = request.GET.get('sort', '')
    songs = sort_songs(songs, sort_by)
    return render(request, 'soundbytes_auth/search.html', {'songs': songs, 'genres': genres})

def stream_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    song.view_count += 1
    song.save()
    return FileResponse(song.audio_file.open(), content_type='audio/mpeg')

def download_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    Download.objects.create(
        user=request.user if request.user.is_authenticated else None,
        song=song
    )
    song.download_count += 1
    song.save()
    filename = song.audio_file.name.split('/')[-1]
    return FileResponse(song.audio_file.open(), as_attachment=True, filename=filename)

@login_required
def toggle_like(request, song_id):
    if request.method != 'POST':
        return redirect(reverse('soundbytes:search_page'))

    song = get_object_or_404(Song, id=song_id)
    like, created = Like.objects.get_or_create(user=request.user, song=song)

    if created:
        song.like_count += 1
    else:
        like.delete()
        song.like_count = max(0, song.like_count - 1)

    song.save()
    return redirect(request.META.get('HTTP_REFERER', reverse('soundbytes:search_page')))

@login_required
def add_comment(request, song_id):
    if request.method == 'POST':
        song = get_object_or_404(Song, id=song_id)
        body = request.POST.get('body', '').strip()
        if body:
            Comment.objects.create(user=request.user, song=song, body=body)

    return redirect(request.META.get('HTTP_REFERER', reverse('soundbytes:search_page')))

@login_required
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        return redirect(reverse('soundbytes:profile') + '?username=' + target_user.username)

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user
    )

    if not created:
        follow.delete()

    return redirect(reverse('soundbytes:profile') + '?username=' + target_user.username)

@login_required
def creator_dashboard(request):
    user_songs = Song.objects.filter(artist=request.user.username).order_by('-upload_date')

    total_views = sum(song.view_count for song in user_songs)
    total_downloads = sum(song.download_count for song in user_songs)
    total_likes = sum(song.like_count for song in user_songs)
    total_comments = Comment.objects.filter(song__in=user_songs).count()
    follower_count = Follow.objects.filter(following=request.user).count()
    profile_view_count = ProfileView.objects.filter(profile_user=request.user).count()

    context = {
        'songs': user_songs,
        'total_views': total_views,
        'total_downloads': total_downloads,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'follower_count': follower_count,
        'profile_view_count': profile_view_count,
    }
    return render(request, 'soundbytes_auth/creatordb.html', context)
