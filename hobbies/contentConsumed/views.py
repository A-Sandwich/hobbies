from django.shortcuts import render, HttpResponse, redirect
from .models import Game, OwnedGame, ConsolePlatform
from .forms import GameForm, ObtainGameForm, ConsolePlatformForm

def index(request):
    return HttpResponse("Hello World!!")

def all_games(request):
    games = Game.objects.order_by('release_date')
    owned_games = OwnedGame.objects.select_related('game').filter(user=request.user)
    consoles = ConsolePlatform.objects.all()
    for game in games:
        if owned_games.filter(game=game).exists():
            game.owned = True
    return render(request, 'games/all.html', {'games': games, 'consoles': consoles, 'form' : ObtainGameForm()})

def new_game(request):
    if request.method == 'POST':
        game_form = GameForm(request.POST)
        game = game_form.save()
        return redirect('games')
    return render(request, 'games/new.html', {'form': GameForm()})

def detail_game(request, game_id):
    game = Game.objects.get(pk=game_id)
    return render(request, 'games/detail.html', {'game': game})

def obtain_game(request):
    game = Game.objects.get(pk=request.POST['game_id'])
    allOwnedGames = OwnedGame.objects.filter(user=request.user)
    alreadyOwned = allOwnedGames.filter(user=request.user, game=game).exists()
    consoles = request.POST.getlist('consoles')
    result = ""
    if not alreadyOwned:
        ownedGame = OwnedGame()
        ownedGame.game = game
        ownedGame.user = request.user
        ownedGame.save()
        for console_id in consoles:
            ownedGame.console_platforms.add(int(console_id))
    return redirect('games')

def new_console_platform(request):
    if request.method == 'POST':
        console_platform_form = ConsolePlatformForm(request.POST)
        console = console_platform_form.save()
        return redirect('games')
    return render(request, 'console_platforms/new.html', {'form': ConsolePlatformForm()})