from django.forms import ModelForm, DateInput
from django import forms
from .models import Game, OwnedGame, ConsolePlatforms

class DateInput(forms.DateInput):
    input_type = 'date'

class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'release_date', 'console_platforms']
        widgets = {
            'release_date' : DateInput()
        }

class ConsolePlatformForm(ModelForm):
    class Meta:
        model = ConsolePlatforms
        fields = ['name']

class ObtainGameForm(ModelForm):
    class Meta:
        model = OwnedGame
        fields = ['game']