from django.db import models
from .custom_user import CustomUser
from .game_configuration import GameConfiguration
from datetime import datetime
from ..storage import TournamentStorage

class Tournament(models.Model):
    '''Classe permettant de creer un tournoi'''
    name = models.CharField(max_length=255)
    register_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    organisator = models.CharField(max_length=255)
    code = models.CharField(max_length=16)
    description = models.CharField(max_length=255, null=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    game_configuration = models.ForeignKey(GameConfiguration, on_delete=models.CASCADE, null=False)
    player_min = models.IntegerField()
    start = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    tournament_status = models.FileField(upload_to='dynamic/tournaments', null=True)

    def get_filename(self) -> str:
        '''Permet d'obtenir le nom du fichier

            Returns: 
                (str): le nom du fichier
        '''
        return f'dynamic/tournaments/{self.id}.json'

    def ongoing(self):
        '''Permet de verifier si le tournois est en cours'''
        ret = False

        if (self.start_date <= datetime.now().date() <= self.end_date and ParticipateTournament.objects.filter(tournament=self).count() >= self.player_min):
            ret = not self.terminated()

        return ret

    def has_started_in_theory(self) -> bool:
        '''Permet de verifier si un tournois est sense etre commence

            Returns:
                (bool): True si le tournois doit etre commence
        '''
        return self.start_date <= datetime.now().date()

    def terminated(self) -> bool:
        '''Renvoie si le tournois est fini

            Returns:
                (bool): True si le tournois est fini
        '''
        ret = False

        if(self.end_date <= datetime.now().date()):
            ret = True

        if not ret:
            if self.tournament_status:
                tl = TournamentStorage.load_tournament(self.tournament_status.path)
                ret = tl.winner is not None

            else:
                ret = False

        return ret

    def __str__(self):
        '''Surcharge de la methode str'''
        return self.name

class ParticipateTournament(models.Model):
    '''Classe permettant de creer une table qui répertorie les joueurs dans un tournoi'''
    person = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    win = models.BooleanField(default=False)
