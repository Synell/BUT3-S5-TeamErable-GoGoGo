from datetime import timedelta
from ...logic import Tile, Vector2

class WatchMove:
    '''Classe permettant de regarder les changements sur une parties sauvegardee'''
    def __init__(self, from_: timedelta, to_: timedelta, player: Tile, player_time: timedelta, eaten_tiles: dict[Tile, int], changes: dict[Tile, tuple[Vector2]]) -> None:
        '''Initialise une nouvelle instance de WatchMove.
        
        Args:
            from_ (timedelta): Timestamp de début.
            to_ (timedelta): Timestamp de fin.
            player (Tile): Joueur.
            player_time (timedelta): Duree du joueur.
            eaten_tiles (dict[Tile, int]): Tuiles mangeées.
            changes (dict[Tile, tuple[Vector2]]): Changements.
        '''
        self._from = from_
        self._to = to_
        self._player = player
        self._player_time = player_time
        self._eaten_tiles = eaten_tiles
        self._changes = changes


    @property
    def from_(self) -> timedelta:
        '''Renvoi le temps de début.'''
        return self._from

    @property
    def to_(self) -> timedelta:
        '''Renvoi le temps de fin.'''
        return self._to

    @property
    def player(self) -> Tile:
        '''Renvoi le joueur.'''
        return self._player

    @property
    def player_time(self) -> timedelta:
        '''Renvoi la duree du joueur.'''
        return self._player_time

    @property
    def eaten_tiles(self) -> dict[Tile, int]:
        '''Renvoi les tuiles mangeées. '''
        return self._eaten_tiles

    @property
    def changes(self) -> dict[Tile, tuple[Vector2]]:
        '''Renvoi les changements. '''
        return self._changes


    def time_overlap(self, timestamp: timedelta) -> bool:
        '''Renvoi True si le timestamp est dans la plage de temps. 
        
        Args:
            timestamp (timedelta): Timestamp.

        Returns:
            bool: True si le timestamp est dans la plage de temps, False sinon.
        '''
        return self._from <= timestamp <= self._to
