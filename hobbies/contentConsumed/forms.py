from django import forms

class GameForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    release_date = forms.DateField(label='Release Date')