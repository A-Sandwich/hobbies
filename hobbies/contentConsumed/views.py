from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Game, OwnedGame, ConsolePlatform
from .forms import GameForm, ObtainGameForm, ConsolePlatformForm
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse("Hello World!!")

@login_required
def all_games(request):
    games = Game.objects.order_by('-release_date')
    owned_games = OwnedGame.objects.select_related('game').filter(user=request.user)
    for game in games:
        if owned_games.filter(game=game).exists():
            game.owned = True
    return render(request, 'games/all.html', {'games': games, 'form' : ObtainGameForm()})

@login_required
def game_create(request):
    if request.method == 'POST':
        game_form = GameForm(request.POST)
        game = game_form.save()
        return redirect('games')
    return render(request, 'games/new.html', {'form': GameForm()})

@login_required
def game_update(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        GameForm(instance=game, data=request.POST).save()
        return redirect('game_detail', pk=game.id)
    form = GameForm(instance=game)
    return render(request, 'games/update.html', {
        'object': game,
        'form': form,
    })

@login_required
def game_detail(request, pk):
    game = Game.objects.get(pk=pk)
    return render(request, 'games/detail.html', {'game': game})

@login_required
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

@login_required
def console_platform_create(request):
    if request.method == 'POST':
        console_platform_form = ConsolePlatformForm(request.POST)
        console = console_platform_form.save()
        return redirect('games')
    return render(request, 'console_platforms/new.html', {'form': ConsolePlatformForm()})

@login_required
def console_platform_update(request, pk):
    console = get_object_or_404(ConsolePlatform, pk=pk)
    if request.method == 'POST':
        ConsolePlatformForm(instance=console, data=request.POST).save()
        return redirect('games')
    form = ConsolePlatformForm(instance=console)
    return render(request, 'console_platforms/update.html', {
        'object': console,
        'form': form,
    })
