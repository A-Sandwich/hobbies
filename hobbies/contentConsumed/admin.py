from django.contrib import admin
from .models import Game, OwnedGame, ConsolePlatform

admin.site.register(Game)
admin.site.register(OwnedGame)
admin.site.register(ConsolePlatform)
