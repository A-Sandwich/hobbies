from django.shortcuts import render, HttpResponse
from .models import Game
from .forms import GameForm

def index(request):
    return HttpResponse("Hello World!!")

def all(request):
    games = Game.objects.order_by('-release_date')
    output = ', '.join([g.title for g in games])
    return HttpResponse(output)

def new(request):
    return render(request, 'new.html', {'form': GameForm()})
