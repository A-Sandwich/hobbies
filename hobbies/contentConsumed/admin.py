from django.contrib import admin
from .models import Game, OwnedGame

admin.site.register(Game)
admin.site.register(OwnedGame)
