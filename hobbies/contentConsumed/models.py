from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=500)
    pub_date = models.DateField('date published', auto_now_add=True)
    release_date = models.DateField(null=True)

    def __str__(self):
        return self.title

class OwnedGame(models.Model):
    pass