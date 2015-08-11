from django import forms
from django.contrib.auth.models import User

from apps.userprofile.models import UserProfile

LANGUAGES = (
    ('English','English'),
    ('Espanol','Espanol'),
    ('Francais','Francais'),
    ('Italiano','Italiano'),
)

class UserProfileForm(forms.ModelForm):
    birthday = forms.DateField()
    birthday.widget.attrs['class'] = 'form-control'
    
    city = forms.CharField(required=False)
    city.widget.attrs['class'] = 'form-control'

    language = forms.ChoiceField(required=False,choices=LANGUAGES)
    language.widget.attrs['class'] = 'form-control'

    class Meta:
        model = UserProfile
        fields = ('birthday', 'country', 'city', 'language')


class UserForm(forms.ModelForm):
    username = forms.CharField()
    username.widget.attrs['class'] = 'form-control'

    email = forms.CharField()
    email.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username', 'email')