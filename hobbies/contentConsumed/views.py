from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Game, OwnedGame, ConsolePlatform
from .forms import GameForm, ObtainGameForm, ConsolePlatformForm
from .utilities import ViewUtility
from django.contrib.auth.decorators import login_required
from datetime import date

@login_required
def all_games(request):
    field = None
    direction = None
    if request.method == 'POST':
        field = request.POST.get('field')
        direction = request.POST.get('direction')
    page = request.GET.get('page')
    paginated_games = ViewUtility.get_games_for_list(field, direction, request.user)
    return render(request, 'games/all.html', {'games': paginated_games.get_page(page), 'title': 'All Games', 'subtitle': '', 'sort_fields': ViewUtility.get_sort_fields()})

def games_releasing_soon(request):
    paginated_games = ViewUtility.get_games_for_list(request.GET.get('field'), request.GET.get('direction'), request.user, date.today())
    page = request.GET.get('page')
    return render(request, 'games/releasing_soon.html', {'games': paginated_games.get_page(page), 'title': 'Games Releasing', 'subtitle': 'Out soon!'})

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
    game = Game.objects.get(pk=request.POST.get('game_id'))
    is_obtaining = request.POST.get('remove') is None
    OwnedGame.toggle_obtain(game, request.user, request.POST.getlist('consoles'), is_obtaining)
    redirect_url = request.POST.get('redirect_url') if request.POST.get('redirect_url') else 'games'
    return redirect(redirect_url)

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
def owned_games_get(request):
    games = Game.objects.filter(ownedgame__user = request.user)
    # todo make the template not require so many args   
    return render(request, 'games/all.html', {'games': games, 'title': 'Owned Games', 'subtitle': 'Nice Collection!', 'all_owned': True, 'redirect_url': 'owned_games'})

@login_required
def owned_game_update(request, pk):
    owned_game = get_object_or_404(OwnedGame, pk=pk)
    if request.method == 'POST':
        OwnedGame(instance=owned_game, data=request.POST).save()
        return redirect('owned_games')
    form = ObtainGameForm(instance=owned_game)
    return render(request, 'owned_game/update.html', {
        'object': owned_game,
        'form': form,
    })