from django import forms

from apps.media.models import Audio, TRACK_CHOICES, Genre, PRIVACY_CHOICES, AudioPlaylist, Video


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

    artist = forms.CharField()
    artist.widget.attrs['class'] = 'form-control'
    artist.widget.attrs['placeholder'] = 'Madeon'

    type = forms.ChoiceField(choices=TRACK_CHOICES, required=False,
                             widget=forms.Select(attrs={
                                 'class': 'selectpicker form-control',
                                 'data-style': 'btn-select'
                             }))
    genre = forms.ModelChoiceField(queryset=Genre.objects.all().order_by("name"),
                                   widget=forms.Select(attrs={
                                       'class': 'selectpicker form-control',
                                       'data-style': 'btn-select'
                                   }))

    bpm = forms.CharField(required=False)
    bpm.widget.attrs['class'] = 'form-control'
    bpm.widget.attrs['placeholder'] = '130'

    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Describe your track', 'rows': 3,
                                                               'class': 'form-control'}))

    privacy = forms.ChoiceField(choices=PRIVACY_CHOICES,
                                widget=forms.Select(attrs={
                                    'class': 'selectpicker form-control',
                                    'data-style': 'btn-select'
                                }))

    cover = forms.FileField()
    cover.widget.attrs['style'] = 'opacity:0;width:100px;height:0;'

    class Meta:
        model = Audio
        fields = ('name', 'artist', 'type', 'genre', 'bpm', 'description', 'privacy', 'cover')


class PlayListForm(forms.ModelForm):
    title = forms.CharField()
    title.widget.attrs['class'] = 'form-control'
    title.widget.attrs['placeholder'] = 'Technicolor (Original Mix)'

    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Describe your playlist', 'rows': 3,
                                                               'class': 'form-control'}))

    cover = forms.FileField()
    cover.widget.attrs['style'] = 'opacity:0;width:100px;height:0;'

    class Meta:
        model = AudioPlaylist
        fields = ('title', 'description', 'cover')

class VideoFileForm(forms.ModelForm):
    video = forms.FileField()
    video.widget.attrs['style'] = 'opacity:0;width:160;height:40px;margin-left:-20px;margin-top:-11px;position:absolute'

    class Meta:
        model = Video
        fields = ('video', )

    def clean_video(self):
        data = self.cleaned_data['video']
        if not data.name.endswith('.mp4'):
            raise forms.ValidationError("You have forgotten about Fred!")

        return data

class VideoForm(forms.ModelForm):
    name = forms.CharField()
    name.widget.attrs['class'] = 'form-control'
    name.widget.attrs['placeholder'] = 'Technicolor (Original Mix)'

    artist = forms.CharField()
    artist.widget.attrs['class'] = 'form-control'
    artist.widget.attrs['placeholder'] = 'Madeon'

    type = forms.ChoiceField(choices=TRACK_CHOICES, required=False,
                             widget=forms.Select(attrs={
                                 'class': 'selectpicker form-control',
                                 'data-style': 'btn-select'
                             }))
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(),
                             widget=forms.Select(attrs={
                                 'class': 'selectpicker form-control',
                                 'data-style': 'btn-select'
                             }))

    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Describe your track', 'rows': 3,
                                                               'class': 'form-control'}))

    privacy = forms.ChoiceField(choices=PRIVACY_CHOICES,
                                widget=forms.Select(attrs={
                                    'class': 'selectpicker form-control',
                                    'data-style': 'btn-select'
                                }))

    cover = forms.FileField()
    cover.widget.attrs['style'] = 'opacity:0;width:100px;height:0;'

    class Meta:
        model = Video
        fields = ('name', 'artist', 'type', 'genre', 'description', 'privacy', 'cover')
