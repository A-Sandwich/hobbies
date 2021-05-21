from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Game, OwnedGame, ConsolePlatform
from .forms import GameForm, ObtainGameForm, ConsolePlatformForm
from hobbies.utilities import ViewUtility
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse("Hello World!!")

@login_required
def all_games(request, afield='release_date'):
    sort_field = request.GET.get('field') if request.GET.get('field') else 'release_date'
    direction = ViewUtility.get_direction(request.GET.get('direction'))
    games = Game.objects.order_by(direction + sort_field)
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
    is_obtaining = request.POST.get('remove') is None
    OwnedGame.toggle_obtain(game, request.user, request.POST.getlist('consoles'), is_obtaining)
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

@login_required
def owned_game_get(request):
    games = Game.objects.filter(ownedgame__user = request.user)
    for game in games:
        game.owned = True
        # todo find a way that I won't need to do this
    # todo I need to be able to change the redirect for the obtain form
    # todo I need to be able to change the title of the games/all.html form
    return render(request, 'games/all.html', {'games': games, 'form' : ObtainGameForm()})