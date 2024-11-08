from .Tile import Tile
from .Vector2 import Vector2
from .GoConstants import GoConstants

class Island:
    '''Île de tuiles.'''

    def __init__(self, tile: Tile, *coords: Vector2) -> None:
        '''Constructeur.

        Args:
            tile (Tile): Tuile de l'île.
            *coords (Vector2): Coordonnées des tuiles.
        '''
        self._tile = tile
        self._coords = tuple(coords)


    @property
    def tile(self) -> Tile:
        '''Renvoie la tuile de l'île.'''
        return self._tile
    
    @property
    def coords(self) -> tuple[Vector2]:
        '''Renvoie les coordonnées des tuiles.'''
        return self._coords


    def add(self, coord: Vector2) -> None:
        '''Ajoute une coordonnée.

        Args:
            coord (Vector2): Coordonnée à ajouter.
        '''
        self._coords += (coord,)


    def __eq__(self, __value: object) -> bool:
        '''Compare deux îles de tuiles.

        Args:
            __value (object): Île de tuiles à comparer.

        Returns:
            bool: True si les îles sont égaux, False sinon.
        '''
        if not isinstance(__value, Island): return False

        return self._tile == __value._tile and set(self._coords) == set(__value._coords)


    def __str__(self) -> str:
        '''Surcharge de str.'''
        return f'Island({self._tile}, {self._coords})'

    def __repr__(self) -> str:
        '''Surcharge de repr.'''
        return str(self)


    def get_arround_tiles(self) -> tuple[Vector2]:
        '''Renvoie les coordonnées des tuiles adjacentes.

        Returns:
            tuple[Vector2]: Coordonnées des tuiles adjacentes.
        '''

        arround_tiles = []
        for coord in self._coords:
            for neighbor in GoConstants.Neighbors:
                arrond_tile = coord + neighbor

                if not arrond_tile in self._coords:
                    arround_tiles.append(arrond_tile)

        return tuple(arround_tiles)


    def contains(self, island: 'Island') -> bool:
        '''Vérifie si l'île contient une autre île.

        Args:
            island (Island): Île à vérifier.

        Returns:
            bool: True si l'île est contenue, False sinon.
        '''
        return set(island._coords).issubset(set(self._coords))


    def overlaps(self, island: 'Island') -> bool:
        '''Vérifie si l'île chevauche une autre île.

        Args:
            island (Island): Île à vérifier.

        Returns:
            bool: True si l'île chevauche, False sinon.
        '''
        return set(island._coords).intersection(set(self._coords)) != set()
