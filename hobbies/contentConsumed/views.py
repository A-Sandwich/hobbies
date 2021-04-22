from django.shortcuts import render, HttpResponse
from .models import Game
from .forms import GameForm

def index(request):
    return HttpResponse("Hello World!!")

def all(request):
    games = Game.objects.order_by('-release_date')
    return render(request, 'all.html', {'games': games})

def new(request):
    if request.method == 'POST':
        game_form = GameForm(request.POST)
        game = game_form.save()
        return render(request, 'new.html', {'form' : GameForm(instance=game)})
    return render(request, 'new.html', {'form': GameForm()})

def detail(request, game_id):
    game = Game.objects.get(pk=game_id)
    return render(request, 'detail.html', {'game': game})