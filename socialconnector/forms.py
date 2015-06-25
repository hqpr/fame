# from django import forms
# from .models import UserPhoto, UserAudio, UserVideo
#
#
# class PhotoForm(forms.ModelForm):
#     class Meta:
#         model = UserPhoto
#         fields = ('image',)
#
#
# class AudioForm(forms.ModelForm):
#     class Meta:
#         model = UserAudio
#         fields = ('audio', 'title', 'type', 'genre', 'description', 'privacy', 'cover')
#
#
# class VideoForm(forms.ModelForm):
#     def clean_video(self):
#         data = self.cleaned_data['video']
#
#         if data.content_type not in ['video/mp4']:
#             raise forms.ValidationError("Only mp4 files allowed")
#
#         return data
#
#     class Meta:
#         model = UserVideo
#         fields = ('video', 'cover')