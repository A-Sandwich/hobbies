from django.forms import ModelForm, DateInput
from django import forms
from .models import Game, OwnedGame

class DateInput(forms.DateInput):
    input_type = 'date'

class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'release_date']
        widgets = {
            'release_date' : DateInput()
        }

class ObtainGameForm(ModelForm):
    class Meta:
        model = OwnedGame
        fields = ['game']