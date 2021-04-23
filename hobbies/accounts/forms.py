from django.forms import ModelForm, DateInput, AuthenticationForm
from django import forms
from django.contrib.auth.models import AnonymousUser

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']