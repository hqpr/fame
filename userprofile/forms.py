from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, ACCOUNT_TYPES, UserSocial
from django_countries import countries


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

    username = forms.CharField()
    username.widget.attrs['class'] = 'form-control'
    username.widget.attrs['placeholder'] = 'Username'

    email = forms.CharField()
    email.widget.attrs['class'] = 'form-control'
    email.widget.attrs['placeholder'] = 'user@example.com'

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
    display_name.widget.attrs['placeholder'] = 'User Name'

    birthday = forms.CharField()
    birthday.widget.attrs['class'] = 'form-control'

    country = forms.ChoiceField(choices=countries, widget=forms.Select(attrs={
        'class': 'selectpicker form-control',
        'data-style': 'btn-select'
    }))
    picture = forms.FileField()
    picture.widget.attrs['style'] = 'opacity:0;width:100px;height:0;'

    class Meta:
        model = UserProfile
        fields = ('account_type', 'display_name', 'birthday', 'country', 'picture')


class UserSocialForm(forms.ModelForm):

    link = forms.CharField(label='None')
    link.widget.attrs['class'] = 'form-control'

    class Meta:
        model = UserSocial
        fields = ('account','link')
