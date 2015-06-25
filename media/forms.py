from django import forms
from .models import Audio, TRACK_CHOICES, GENRE_CHOICES, PRIVACY_CHOICES


class AudioFileForm(forms.ModelForm):
    audio = forms.FileField()
    audio.widget.attrs['style'] = 'opacity:0;width:160;height:40px;margin-left:-20px;margin-top:-11px;position:absolute'

    class Meta:
        model = Audio
        fields = ('audio', )

class AudioForm(forms.ModelForm):
    name = forms.CharField()
    name.widget.attrs['class'] = 'form-control'
    name.widget.attrs['placeholder'] = 'Technicolor (Original Mix)'

    user = forms.CharField()
    user.widget.attrs['class'] = 'form-control'
    name.widget.attrs['placeholder'] = 'Madeon'

    type = forms.ChoiceField(choices=TRACK_CHOICES,
                             widget=forms.Select(attrs={
                                 'class': 'selectpicker form-control',
                                 'data-style': 'btn-select'
                             }))
    genre = forms.ChoiceField(choices=GENRE_CHOICES,
                             widget=forms.Select(attrs={
                                 'class': 'selectpicker form-control',
                                 'data-style': 'btn-select'
                             }))

    bpm = forms.CharField()
    bpm.widget.attrs['class'] = 'form-control'
    bpm.widget.attrs['placeholder'] = '130'

    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Describe your track', 'rows': 3,
                                                               'class': 'form-control'}))

    privacy = forms.ChoiceField(choices=PRIVACY_CHOICES,
                                widget=forms.Select(attrs={
                                    'class': 'selectpicker form-control',
                                    'data-style': 'btn-select'
                                }))

    # cover = forms.FileField()
    # cover.widget.attrs['style'] = 'opacity:0;width:100px;height:0;'

    class Meta:
        model = Audio
        fields = ('name', 'type', 'genre', 'bpm', 'description', 'privacy', 'cover')
