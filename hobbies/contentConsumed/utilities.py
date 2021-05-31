from .models import Game, OwnedGame
from django.core.paginator import Paginator

class ViewUtility:
    @staticmethod
    def get_direction(direction, default='descending'):
        direction = default if not direction else direction
        # '-' is specific to django query order
        return '-' if direction.lower() == 'descending' else ''

    @staticmethod
    def get_games_for_list(sort_field, direction, user, date=None, page_size=100):
        sort_field = sort_field if sort_field else 'release_date'
        direction = ViewUtility.get_direction(direction)
        games = Game.objects.order_by(direction + sort_field)
        if date:
            games = games.filter(release_date__gte=date)
        owned_games = OwnedGame.objects.select_related('game').filter(user=user)
        for game in games:
            owned_game = owned_games.filter(game=game)
            if owned_game.exists():
                game.owned = owned_game[0].id
        return Paginator(games, page_size)
    
    @staticmethod
    def get_sort_fields():
        return [
            "title",
            "release_date",
        ]