from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published')
