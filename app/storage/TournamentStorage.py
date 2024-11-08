from ..tournament_logic import Tournament
import json, os

class TournamentStorage:
    def __new__(cls) -> None:
        '''Fait en sorte que la classe ne puisse pas être instanciée'''
        return None
    
    @staticmethod
    def load_tournament(path: str) -> Tournament:
        '''Charge un tournois depuis la base de données

        Args:
            path (str): Le chemin vers le tournois

        Returns:
            Tournament: Le tournois
        '''
        with open(path, 'r', encoding = 'utf-8') as f:
            tournament = Tournament(json.load(f))

        return tournament

    @staticmethod
    def save_tournament(path: str, tournament: Tournament) -> None:
        '''Sauvegarde un tournois dans la base de données

        Args:
            path (str): Le chemin vers le tournois
            tournament (Tournament): Le tournois
        '''
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        with open(path, 'w', encoding = 'utf-8') as f:
            json.dump(tournament.export(), f)
