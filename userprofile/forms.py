from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserForm(forms.ModelForm):
    username = forms.CharField()
    username.widget.attrs['class'] = 'form-control'
    username.widget.attrs['placeholder'] = 'alexpluda'

    email = forms.CharField()
    email.widget.attrs['class'] = 'form-control'
    email.widget.attrs['placeholder'] = 'e.g. johnappleseed@dummy.com'

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '......a'
    }))

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('account_type', 'display_name', 'country', 'picture',)