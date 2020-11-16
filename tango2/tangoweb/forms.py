from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    SCHOOL_CHOICE =( 
        ("PRIMARY", "Primary"), 
        ("SECONDARY", "Secondary"), 
        ("SIXTH_FORM", "Sixth Form"), 
    ) 
    school_stage = forms.ChoiceField(
        choices = SCHOOL_CHOICE,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = UserProfile
        fields = ['school_stage']