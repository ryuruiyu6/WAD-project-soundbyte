from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Profile,Playlist

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password',)

    def clean(self):
        data = super().clean()
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password Mismatch")
        return data

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('artist_name','profile_picture','user_type','bio')

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['title']  # only the playlist title is needed
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Playlist Title'}),
        }
        labels = {
            'title': 'Playlist Name',
        }