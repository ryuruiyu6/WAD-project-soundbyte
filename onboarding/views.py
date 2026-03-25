from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def landing(request):
    return render(request, "onboarding/landing.html")

def register(request):
    return render(request, "onboarding/register.html")

def sign_in(request):
    return render(request, "onboarding/sign-in.html")