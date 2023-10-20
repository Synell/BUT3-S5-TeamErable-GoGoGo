from django.db import models
from .custom_user import CustomUser
import datetime

class Tournament(models.Model):
    name = models.CharField(max_length=255)
    register_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    organisator = models.CharField(max_length=255)
    code = models.CharField(max_length=16)
    description = models.CharField(max_length=255, null=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    player_min = models.IntegerField()
    start = models.BooleanField(default=False)
    private = models.BooleanField(default=False)

    #Permet de verifier si le tournois est en cours
    def ongoing(self):
        if(self.start_date <= datetime.datetime.now().date() <= self.end_date): return True
        else: return False

    def __str__(self):
        return self.name

class Participate(models.Model):
    person = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    win = models.BooleanField(default=False)