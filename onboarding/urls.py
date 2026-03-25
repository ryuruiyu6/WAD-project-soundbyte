from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="blank"),
    path("landing/", views.landing, name="landing"),
    path("register/", views.register, name="register"),
    path("sign-in/", views.sign_in, name="sign-in")
]