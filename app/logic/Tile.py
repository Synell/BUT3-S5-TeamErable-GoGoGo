from enum import Enum
from .TileColor import TileColor

class Tile(Enum):
    '''Tuile du plateau de jeu.'''

    White = TileColor('⚪', 'white')
    Black = TileColor('⚫', 'black')


    def __str__(self) -> str:
        '''Surchage de la méthode str'''
        return str(self.value)


    @staticmethod
    def from_value(value: str) -> 'Tile | None':
        '''Convertit une chaîne de caractères en une tuile.

        Args:
            value (str): Chaîne de caractères à convertir.

        Returns:
            Tile | None: Tuile correspondante ou None si la chaîne n'est pas valide.
        '''
        for tile in Tile:
            if tile.value.value == value:
                return tile
        return None


    @staticmethod
    def from_color(color: str) -> 'Tile | None':
        '''Convertit une couleur en une tuile.

        Args:
            color (str): Couleur à convertir.

        Returns:
            Tile | None: Tuile correspondante ou None si la couleur n'est pas valide.
        '''
        for tile in Tile:
            if tile.value.color == color:
                return tile
        return None


    @property
    def next(self) -> 'Tile':
        '''Renvoie la tuile suivante.

        Returns:
            Tile: Tuile suivante.
        '''
        l = list(Tile)
        return l[(l.index(self) + 1) % len(l)]
