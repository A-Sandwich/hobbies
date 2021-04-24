from django.shortcuts import render, HttpResponse
from .models import Game, OwnedGame
from .forms import GameForm, ObtainGameForm

def index(request):
    return HttpResponse("Hello World!!")

def all(request):
    games = Game.objects.order_by('-release_date')
    owned_games = OwnedGame.objects.select_related('game').filter(user=request.user)
    for game in games:
        if owned_games.filter(game=game).exists():
            game.owned = True
    return render(request, 'all.html', {'games': games, 'form' : ObtainGameForm()})

def new(request):
    if request.method == 'POST':
        game_form = GameForm(request.POST)
        game = game_form.save()
        return render(request, 'new.html', {'form' : GameForm(instance=game)})
    return render(request, 'new.html', {'form': GameForm()})

def detail(request, game_id):
    game = Game.objects.get(pk=game_id)
    return render(request, 'detail.html', {'game': game})

def obtain(request):
    game = Game.objects.get(pk=request.POST['game_id'])
    allOwnedGames = OwnedGame.objects.filter(user=request.user)
    alreadyOwned = allOwnedGames.filter(user=request.user, game=game).exists()
    result = ""
    if not alreadyOwned:
        ownedGame = OwnedGame()
        ownedGame.game = game
        ownedGame.user = request.user
        ownedGame.save()

    #just outputting this for now, will delete:
    for g in allOwnedGames:
        result += str(g) +", "
    
    return HttpResponse(result)