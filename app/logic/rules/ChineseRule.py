from .RuleBase import RuleBase, Board, Tile
from .RuleFactory import RuleFactory
from .JapaneseRule import JapaneseRule

class ChineseRule(RuleBase):
    '''Règle chinoise.'''

    key: str = 'chinese'

    def __init__(self, board: Board, komi: float) -> None:
        '''Initialise une régle chinoise.

        Args:
            board (Board): Plateau de jeu.
            komi (float): Komi.
        '''
        super().__init__(board, komi)

    def count_points(self) -> dict[Tile, float]:
        '''Compte les points selon la règle chinoise.

        On compte les territoires et les pierres qui dessinent les territoires.

        Args:
            board (Board): Plateau de jeu.

        Returns:
            dict[Tile, int]: Points des joueurs.
        '''
        
        total = JapaneseRule(self.board, self.komi).count_points()

        checked: list[list[bool]] = [[False for _ in range(self.board.size.x)] for _ in range(self.board.size.y)]

        territories = self.board.get_territories()

        for t in Tile:
            for territory in territories[t]:
                for pion in territory.get_arround_tiles():
                    if self.board.is_outside(pion): continue
                    if checked[pion.y][pion.x]: continue
                    checked[pion.y][pion.x] = True

                    if territory.tile == Tile.White:
                        total[Tile.White] += 1

                    if territory.tile == Tile.Black:
                        total[Tile.Black] += 1

        return total


RuleFactory().register(ChineseRule)
