from django import forms
from .models import Website
class WebsiteForm(forms.Form):
    name=forms.CharField(max_length=100)
    url=forms.URLField()