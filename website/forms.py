from django import forms
from .models import Website
class WebsiteForm(forms.Form):
    name=forms.CharField(max_length=100)
    url=forms.URLField()
    redirect_url=forms.URLField()
class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control',}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control',}))