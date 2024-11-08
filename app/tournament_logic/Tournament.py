from .match.Bracket import Bracket
from .match.MatchFactory import MatchFactory
from .match.IMatch import IMatch
from .Player import Player
from plum import dispatch as overload

class Tournament:
    '''Représente un tournoi de jeu de go'''

    @overload
    def __init__(self, players: list[Player]) -> None:
        '''Initialise un tournoi

        Args:
            players (list[Player]): Les joueurs du tournoi
        '''
        self._players = list(players)
        self._bracket = self._generate_bracket(self._players)


    @overload
    def __init__(self, data: dict) -> None:
        '''Initialise un tournoi à partir d'un dictionnaire

        Args:
            data (dict): Le dictionnaire contenant les données du tournoi
        '''
        self._players = [Player(id) for id in data['players']]
        self._bracket = MatchFactory.import_(data['bracket'])


    @property
    def players(self) -> list[Player]:
        '''Renvoie la liste des joueurs du tournoi'''
        return self._players

    @property
    def bracket(self) -> IMatch:
        '''Renvoie le bracket du tournoi'''
        return self._bracket

    @property
    def winner(self) -> Player:
        '''Renvoie le vainqueur du tournoi'''
        return self._bracket.winner


    def _generate_bracket(self, players: list[Player]) -> IMatch:
        '''Génère un bracket à partir d'une liste de joueurs

        Args:
            players (list[Player]): Les joueurs du bracket

        Returns:
            IMatch: Le bracket
        '''
        ret = None

        length = len(players)
        if length <= 2: ret = MatchFactory.build_match(*players)
        else: ret = Bracket(self._generate_bracket(players[:length // 2]), self._generate_bracket(players[length // 2:]))

        return ret


    def __str__(self) -> str:
        '''Retourne une représentation du tournoi sous forme de chaîne de caractères

        Returns:
            str: La représentation du tournoi
        '''
        s = '\t' + str(self._bracket).replace('\n', '\n\t')
        return f'{__class__.__name__}(\n{s}\n)'.replace('\t', ' ' * 4)


    def __repr__(self) -> str:
        '''Retourne une représentation du tournoi sous forme de chaîne de caractères

        Returns:
            str: La représentation du tournoi
        '''
        return str(self)


    def do_win(self, player: Player) -> None:
        '''Indique qu'un joueur a gagné

        Args:
            player (Player): Le joueur qui a gagné
        '''
        self._bracket.do_win(player)


    def get_current_matches(self) -> list[IMatch]:
        '''Retourne les matchs en cours

        Returns:
            list[IMatch]: Les matchs en cours
        '''
        return self._bracket.get_current_matches()


    def export(self) -> dict:
        '''Exporte le tournoi au format JSON

        Returns:
            dict: Le tournoi au format JSON
        '''
        ret = {
            'players': [player.id for player in self._players],
            'bracket': self._bracket.export(),
        }

        return ret
