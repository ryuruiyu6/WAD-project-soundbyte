from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from django.http import JsonResponse
from .functions.file_manager import create_song
from .functions.search_function import search, sort_songs
from django.views.decorators.csrf import csrf_exempt
from .forms import UserForm,ProfileForm

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
    return redirect(reverse('rango:index'))

def home(request):
    return None

def profile(request):
    return None

@csrf_exempt
def upload_song(request):
    if request.method == 'POST':
        song = create_song(request.POST, request.FILES)
        return JsonResponse({'status': 'success', 'song_id': song.id})

    return JsonResponse({'error': 'Invalid request'})

@csrf_exempt
def search_songs(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '')

    songs = search(query)
    songs = sort_songs(songs, sort_by)

    return JsonResponse(list(songs.values()), safe=False)
