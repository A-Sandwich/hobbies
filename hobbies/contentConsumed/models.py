from django.db import models
from django.conf import settings

class Game(models.Model):
    title = models.CharField(max_length=500)
    pub_date = models.DateField('date published', auto_now_add=True)
    release_date = models.DateField(null=True)
    owned = False

    def __str__(self):
        return self.title

class OwnedGame(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + " Owns " + str(self.game)
