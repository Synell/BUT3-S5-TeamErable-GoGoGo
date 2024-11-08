from interface import Interface
from ..Player import Player

class IMatch(Interface):
    @property
    def winner(self) -> Player | None:
        pass

    @property
    def player1(self) -> Player | None:
        pass

    @property
    def player2(self) -> Player | None:
        pass


    def do_win(self, player: Player) -> None:
        '''Indique qu'un joueur a gagné

        Args:
            player (Player): Le joueur qui a gagné
        '''
        pass


    def get_current_matches(self) -> list['IMatch']:
        '''Retourne les matchs en cours

        Returns:
            list[IMatch]: Les matchs en cours
        '''
        pass


    def __str__(self) -> str:
        '''Retourne une représentation du match sous forme de chaîne de caractères

        Returns:
            str: La représentation du match
        '''
        pass

    def __repr__(self) -> str:
        '''Retourne une représentation du match sous forme de chaîne de caractères

        Returns:
            str: La représentation du match
        '''
        pass


    def export(self) -> dict:
        '''Exporte le match au format JSON

        Returns:
            dict: Le match au format JSON
        '''
        pass
