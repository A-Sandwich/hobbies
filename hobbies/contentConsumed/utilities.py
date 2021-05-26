from .models import Game, OwnedGame

class ViewUtility:
    @staticmethod
    def get_direction(direction, default='desc'):
        direction = default if not direction else direction
        # '-' is specific to django query order
        return '-' if direction.lower() == 'desc' else ''

    @staticmethod
    def get_games_for_list(sort_field, direction, user, date=None):
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
        return games