from django import forms
from .models import Music, Artist

class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['title', 'artist', 'duration', 'file_url', 'cover']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'artist': forms.Select(attrs={'class': 'form-input'}),
            'duration': forms.TextInput(attrs={'class': 'form-input'}),
            'file_url': forms.URLInput(attrs={'class': 'form-input'}),
            'cover': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }
