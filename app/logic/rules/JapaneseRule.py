from .RuleBase import RuleBase, Board, Tile
from .RuleFactory import RuleFactory

class JapaneseRule(RuleBase):
    '''Règle japonaise.'''

    key: str = 'japanese'

    def __init__(self, board: Board, komi: float) -> None:
        '''Initialise une régle japonaise.

        Args:
            board (Board): Plateau de jeu.
            komi (float): Komi.
        '''
        super().__init__(board, komi)

    def count_points(self) -> dict[Tile, float]:
        '''Compte les points selon la règle japonaise.

        On compte seulement les territoires.
        Les pionts du joueur b qui sont dans les territoires du joueur a, sont ajoutés pour le score du joueur a.
        Les cases vides compris dans le territoire du joueur a sont ajoutés pour le score du joueur a.

        Returns:
            dict[Tile, int]: Points des joueurs.
        '''
        territories = self.board.get_territories()

        score_black = 0
        score_white = 0

        for t in territories:
            for territory in territories[t]:
                for pion in territory.coords:
                    if territory.tile == Tile.White:
                        if self.board.get(pion) == Tile.Black: 
                            score_white += 1

                        if self.board.get(pion) == None: 
                            score_white += 1

                    if territory.tile == Tile.Black:
                        if self.board.get(pion) == Tile.White: 
                            score_black += 1

                        if self.board.get(pion) == None: 
                            score_black += 1

        score_black += self.board.komi

        return {
            Tile.Black: score_black,
            Tile.White: score_white
        }

RuleFactory().register(JapaneseRule)
