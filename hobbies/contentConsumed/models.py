from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class ConsolePlatform(models.Model):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=10, null=True)
    tag_color = models.CharField(max_length=10, null=True)
 
    # this returns bulma specific tag colors
    def tag_class(self):
        if not self.tag_color:
            return

        tag_color = self.tag_color.lower()
        if tag_color == 'red':
            return 'is-danger'
        elif tag_color == 'green':
            return 'is-success'
        elif tag_color == 'blue':
            return 'is-info'
        elif tag_color == 'white':
            return 'is-white'
        else:
            return ''

    def __str__(self):
        return self.name

class Game(models.Model):
    title = models.CharField(max_length=500)
    pub_date = models.DateField('date published', auto_now_add=True)
    release_date = models.DateField(null=True)
    console_platforms = models.ManyToManyField(ConsolePlatform)
    owned = False

    def __str__(self):
        return self.title

class OwnedGame(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    console_platforms = models.ManyToManyField(ConsolePlatform)

    def __str__(self):
        return str(self.user) + " Owns " + str(self.game)
