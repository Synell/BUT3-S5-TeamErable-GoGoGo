from interface import implements
from .IMatch import IMatch
from ..Player import Player
from . import MatchFactory

class Bracket(implements(IMatch)):
    '''Bracket entre deux matchs

    Args:
        implements (_type_): Interface IMatch
    '''

    def __init__(self, bracket1: IMatch, bracket2: IMatch) -> None:
        '''Initialise un bracket

        Args:
            bracket1 (IMatch): Bracket 1
            bracket2 (IMatch): Bracket 2
        '''
        self._id: int = None
        self._bracket1 = bracket1
        self._bracket2 = bracket2
        self._winner: Player | None = None


    @property
    def id(self) -> int:
        '''Renvoie l'id du match'''
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        '''Modifie l'id du match
        
        Args:
            value (int): Nouvel id

        Raises:
            Exception: L'id est déjà utilisé / déja utilisé par un match
        '''
        if self._id is not None: raise Exception('Match id is already set')
        self._id = value

    @property
    def bracket1(self) -> IMatch:
        '''Renvoie le bracket 1'''
        return self._bracket1

    @property
    def bracket2(self) -> IMatch:
        '''Renvoie le bracket 2'''
        return self._bracket2

    @property
    def player1(self) -> Player | None:
        '''Renvoie le gagnant du bracket 1'''
        return self._bracket1.winner if self._bracket1.winner is not None else None

    @property
    def player2(self) -> Player | None:
        '''Renvoie le gagnant du bracket 2'''
        return self._bracket2.winner if self._bracket2.winner is not None else None

    @property
    def winner(self) -> Player | None:
        '''Renvoie le gagnant du bracket'''
        return self._winner


    def __str__(self) -> str:
        '''Surchage de la méthode str'''
        if self._winner is not None: ret = f'{self._winner}'
        else:
            addon = ' -> Match' if self._bracket1.winner is not None and self._bracket2.winner is not None else ''
            s1 = '\t' + str(self._bracket1).replace('\n', '\n\t')
            s2 = '\t' + str(self._bracket2).replace('\n', '\n\t')
            ret = f'{__class__.__name__}{addon}(\n{s1},\n{s2}\n)'

        return ret

    def __repr__(self) -> str:
        '''Surchage de la méthode repr'''
        return str(self)


    def do_win(self, player: Player) -> None:
        '''Fait gagner un joueur

        Args:
            player (Player): Joueur gagnant
        '''
        ret = False
        if (self._bracket1.winner is None):
            self._bracket1.do_win(player)
            ret = True

        if (self._bracket2.winner is None):
            self._bracket2.do_win(player)
            ret = True

        if not ret:
            if (self._bracket1.winner == player): self._winner = self._bracket1.winner
            elif (self._bracket2.winner == player): self._winner = self._bracket2.winner


    def get_current_matches(self) -> list[IMatch]:
        '''Renvoie les matchs en cours

        Returns:
            list[IMatch]: Liste des matchs en cours
        '''
        ret = []

        if (self._bracket1.winner is None): ret += self._bracket1.get_current_matches()
        if (self._bracket2.winner is None): ret += self._bracket2.get_current_matches()

        if self._bracket1.winner is not None and self._bracket2.winner is not None and self._winner is None: ret.append(self)

        return ret


    def export(self) -> dict:
        '''Exporte le bracket vers un dictionnaire

        Returns:
            dict: Le dictionnaire contenant le bracket
        '''
        return {
            'type': 'Bracket',
            'id': self._id,
            'brackets': [self._bracket1.export(), self._bracket2.export()],
            'winner': self._winner.id if self._winner is not None else None
        }


    @staticmethod
    def import_(data: dict) -> IMatch:
        '''Importe un bracket depuis un dictionnaire

        Args:
            data (dict): Le dictionnaire contenant le bracket

        Returns:
            IMatch: Le bracket
        '''
        brackets = [MatchFactory.MatchFactory.import_(bracket) for bracket in data['brackets']]
        ret = Bracket(*brackets)
        ret.id = data['id']
        ret._winner = Player(data['winner']) if data.get('winner', None) is not None else None
        return ret
