from django.db import models
from ..models import CustomUser

class GameSave(models.Model):
    '''Classe permettant de creer une table qui répertorie les parties sauvegardées'''
    id_game_save = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    name = models.CharField(max_length=255, null=False)
    player1 = models.CharField(max_length=255, null=False)
    player2 = models.CharField(max_length=255, null=False)
    score_player1 = models.FloatField(default=0.0, null=False)
    score_player2 = models.FloatField(default=0.0, null=False)
    duration = models.IntegerField(null=False)
    move_list = models.TextField(null=False)
    tournament = models.CharField(max_length=255, null=True)
    map_size = models.IntegerField(null=False)
    komi = models.FloatField(null=False)
    counting_method = models.CharField(max_length=255, null=False)
    clock_type = models.CharField(max_length=255, null=False)
    clock_value = models.IntegerField(null=False)
    byo_yomi = models.IntegerField(null=False)
    handicap = models.IntegerField(null=False)