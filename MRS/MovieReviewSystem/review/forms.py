from django import forms
from django.core.validators import FileExtensionValidator

class LoginForm(forms.Form):
    Username = forms.CharField(max_length=70, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'user_name'}))
    password = forms.CharField(min_length=8, max_length=18, widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password'}))

class MovieForm(forms.Form):
    movietitle = forms.CharField(max_length=20,required = True,widget=forms.TextInput(attrs={'size': 30}))
    poster = forms.FileField(required=True)
    synopsis = forms.CharField(max_length=500,required = True,widget=forms.TextInput(attrs={'size': 30}))