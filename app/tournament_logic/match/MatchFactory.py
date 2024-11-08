from .Match import Match
from .FakeMatch import FakeMatch
from .Bracket import Bracket
from .IMatch import IMatch
from ..Player import Player

class MatchFactory:
    '''Fabrique de matchs'''

    def __new__(cls) -> None:
        '''Empêche l'instanciation de la classe'''
        return None


    @staticmethod
    def build_match(*players: Player) -> IMatch:
        '''Construit un match à partir d'une liste de joueurs

        Raises:
            ValueError: Pas de joueurs
            ValueError: Nombre invalide de joueurs

        Returns:
            IMatch: Le match
        '''
        res = None

        match len(players):
            case 0: raise ValueError('No players')
            case 1: res = FakeMatch(players[0])
            case 2: res = Match(players[0], players[1])
            case _: raise ValueError('Invalid number of players')

        return res


    @staticmethod
    def import_(data: dict) -> IMatch:
        '''Importe un match depuis un dictionnaire

        Args:
            data (dict): Le dictionnaire contenant le match

        Returns:
            IMatch: Le match
        '''
        res = None

        match data['type']:
            case 'Bracket': res = Bracket.import_(data)
            case 'Match': res = Match.import_(data)
            case 'FakeMatch': res = FakeMatch.import_(data)
            case _: raise ValueError('Invalid match type')

        return res
