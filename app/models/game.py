from django.db import models
from .game_participate import GameParticipate
from . import Tournament
from .game_configuration import GameConfiguration

class Game(models.Model):
    '''Classe permettant de creer une partie'''
    id_game = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    code = models.CharField(max_length=16, null=True)
    start_date = models.DateField()
    duration = models.IntegerField()
    done = models.BooleanField(default=False)
    move_list = models.FileField(upload_to='dynamic/games', null=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='tournament', null=True)
    game_configuration = models.ForeignKey(GameConfiguration, on_delete=models.CASCADE, null=False)
    game_participate = models.ForeignKey(GameParticipate, on_delete=models.CASCADE, null=True)