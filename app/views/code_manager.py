import random
import string
from django.db.models import QuerySet
from ..models.game import Game
from ..models.tournament import Tournament
from datetime import datetime

# Classe qui s'occupe de la gestion des codes unique des parties et tournois
class CodeManager:
    
    def generate_game_code(self) -> str:
        '''Methode generant un code unique pour une partie

        Returns:
            str: Un code unique

        '''
        code = None
        while (code is None or Game.objects.filter(code=code, done=False).exists()):
            code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        return code

    def generate_tournament_code(self) -> str:
        '''Methode generant un code unique pour un tournoi

        Returns:
            str: Un code unique

        '''
        code = None
        while (code is None or Tournament.objects.filter(code=code, end_date__gt = datetime.now()).exists()):
            code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        return code