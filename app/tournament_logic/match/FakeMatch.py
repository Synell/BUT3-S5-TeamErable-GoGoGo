from interface import implements
from .IMatch import IMatch
from ..Player import Player

class FakeMatch(implements(IMatch)):
    '''Faux match, utilisé pour l'attente du prochain round

    Args:
        implements (_type_): Interface IMatch
    '''

    def __init__(self, player: Player) -> None:
        '''Initialise un match fictif

        Args:
            player (Player): Le joueur qui est seul dans le match
        '''
        self._player = player


    @property
    def player(self) -> Player:
        '''Renvoie le joueur'''
        return self._player

    @property
    def winner(self) -> Player | None:
        '''Renvoie le gagnant, hérite de IMatch'''
        return self._player

    @property
    def player1(self) -> Player | None:
        '''Renvoie le joueur, hérite de IMatch'''
        return self._player

    @property
    def player2(self) -> Player | None:
        '''Renvoie le joueur, hérite de IMatch'''
        return None


    def __str__(self) -> str:
        '''Surcharge de la méthode str'''
        return 'FakeMatch -> ' + str(self._player)

    def __repr__(self) -> str:
        '''Surcharge de la méthode repr'''
        return str(self)


    def do_win(self, player: Player) -> None:
        pass


    def get_current_matches(self) -> list[IMatch]:
        return []


    def export(self) -> dict:
        '''Exporte le match
        
        Returns:
            dict: Le match
        '''
        return {
            'type': 'FakeMatch',
            'player': self._player.id,
        }


    def import_(data: dict) -> IMatch:
        '''Importe un match fictif

        Args:
            data (dict): Le match fictif au format JSON

        Returns:
            IMatch: Le match fictif
        '''
        return FakeMatch(Player(data['player']))
