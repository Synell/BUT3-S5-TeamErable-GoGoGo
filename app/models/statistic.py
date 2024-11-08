from django.db import models

class Statistic(models.Model):
    '''Classe permettant de creer une table qui répertorie les statistiques des joueurs'''
    game_win = models.IntegerField(default=0)
    game_loose = models.IntegerField(default=0)
    game_ranked_win = models.IntegerField(default=0)
    game_ranked_loose = models.IntegerField(default=0)
    tournament_win = models.IntegerField(default=0)
    tournament_loose = models.IntegerField(default=0)
    elo = models.IntegerField(default=1000)
    rank = models.CharField(max_length=100, default="30ème Kyu")






