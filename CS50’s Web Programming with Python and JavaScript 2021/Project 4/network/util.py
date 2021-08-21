from . import models
from django import forms

class NewPostForm (forms.Form):
    content = forms.CharField(label="New Post", max_length=240, min_length=1, required=True, widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'rows': '5',
            'placeholder': "What's going on?"
        }
    ))

