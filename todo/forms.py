from django.forms import ModelForm
from django import forms
from .models import Todo, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'important']

class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required= True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        unique_together = ['username', 'email']

class ChangeUserProfile(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']


