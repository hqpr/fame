from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, ACCOUNT_TYPES
from django_countries import countries


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '......a'
    }))

    username = forms.CharField()
    username.widget.attrs['class'] = 'form-control'
    username.widget.attrs['placeholder'] = 'alexpluda'

    email = forms.CharField()
    email.widget.attrs['class'] = 'form-control'
    email.widget.attrs['placeholder'] = 'e.g. johnappleseed@dummy.com'

    class Meta:
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPES, widget=forms.RadioSelect())

    display_name = forms.CharField()
    display_name.widget.attrs['class'] = 'form-control'
    display_name.widget.attrs['placeholder'] = 'Alex Pluda'

    birthday = forms.CharField()
    birthday.widget.attrs['class'] = 'form-control'

    country = forms.ChoiceField(choices=countries, widget=forms.Select(attrs={
        'class': 'selectpicker form-control',
        'data-style': 'btn-select'
    }))

    class Meta:
        model = UserProfile
        fields = ('account_type', 'display_name', 'birthday', 'country', 'picture')