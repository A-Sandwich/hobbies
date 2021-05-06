from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class ConsolePlatforms(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return name

class Game(models.Model):
    title = models.CharField(max_length=500)
    pub_date = models.DateField('date published', auto_now_add=True)
    release_date = models.DateField(null=True)
    console_platforms = models.ManyToManyField(ConsolePlatforms)

    def __str__(self):
        return self.title

class OwnedGame(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    console_platforms = models.ManyToManyField(ConsolePlatforms)

    def __str__(self):
        return str(self.user) + " Owns " + str(self.game)

