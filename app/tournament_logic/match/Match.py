from interface import implements
from .IMatch import IMatch
from ..Player import Player

class Match(implements(IMatch)):
    '''Match entre deux joueurs

    Args:
        implements (_type_): Interface IMatch
    '''

    def __init__(self, player1: Player, player2: Player) -> None:
        '''Initialise un match

        Args:
            player1 (Player): Joueur 1
            player2 (Player): Joueur 2
        '''
        self._id: int = None
        self._player1: Player = player1
        self._player2: Player = player2
        self._winner: Player = None


    @property
    def id(self) -> int:
        '''Renvoie l'id du match'''
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        '''Définit l'id du match

        Args:
            value (int): Nouvel id

        Raises:
            Exception: L'id est déjà utilisé / déja utilisé par un match
        '''
        if self._id is not None: raise Exception('Match id is already set')
        self._id = value

    @property
    def player1(self) -> Player:
        '''Renvoie le joueur 1'''
        return self._player1

    @property
    def player2(self) -> Player:
        '''Renvoie le joueur 2'''
        return self._player2

    @property
    def winner(self) -> Player | None:
        '''Renvoie le gagnant du match'''
        return self._winner


    def __str__(self) -> str:
        '''Surcharge de la méthode str'''
        ret = ''
        if self._winner is not None:
            ret = str(self._winner)

        else:
            s1 = '\t' + str(self._player1).replace('\n', '\n\t')
            s2 = '\t' + str(self._player2).replace('\n', '\n\t')
            ret = f'{__class__.__name__}(\n{s1},\n{s2}\n)'

        return ret

    def __repr__(self) -> str:
        '''Surcharge de la méthode repr'''
        return str(self)


    def do_win(self, player: Player) -> None:
        '''Fait gagner le match

        Args:
            player (Player): Joueur gagnant
        '''
        if player == self._player1: self._winner = self._player1
        elif player == self._player2: self._winner = self._player2


    def get_current_matches(self) -> list[IMatch]:
        '''Renvoie la liste des matchs en cours
        
        Returns:
            list[IMatch]: La liste des matchs
        '''
        return [self]


    def export(self) -> dict:
        '''Exporte le match

        Returns:
            dict: Le match
        '''
        return {
            'type': 'Match',
            'id': self._id,
            'players': [self._player1.id, self._player2.id],
            'winner': self._winner.id if self._winner is not None else None,
        }


    @staticmethod
    def import_(data: dict) -> IMatch:
        '''Importe un match

        Args:
            data (dict): Le match au format JSON

        Returns:
            IMatch: Le match
        '''
        players = [Player(id) for id in data['players']]
        ret = Match(*players)
        ret.id = data['id']
        if data['winner'] is not None: ret._winner = Player(data['winner'])

        return ret
