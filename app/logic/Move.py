from .Vector2 import Vector2
from datetime import timedelta
from plum import dispatch as overload

class Move:
    '''Classe représentant un mouvement.'''

    @overload
    def __init__(self, pos: Vector2 | None, timestamp: timedelta) -> None:
        '''Constructeur de la classe Move.

        Args:
            pos (Vector2 | None): Position du mouvement.
            timestamp (timedelta): Temps du mouvement.
        '''
        self._pos = pos
        self._timestamp = timestamp

    @overload
    def __init__(self, data: str) -> None:
        '''Constructeur de la classe Move.

        Args:
            data (str): CSV du mouvement.
        '''
        x, y, time = data.split(';')
        self._pos = Vector2(float(x), float(y)) if x != '' and y != '' else None
        self._timestamp = timedelta(seconds = float(time))


    @property
    def pos(self) -> Vector2 | None:
        '''Renvoi la position du mouvement.'''
        return self._pos

    @property
    def time(self) -> timedelta:
        '''Renvoi le temps du mouvement. '''
        return self._timestamp


    def __str__(self) -> str:
        '''Représentation du mouvement.

        Returns:
            str: Représentation du mouvement.
        '''
        return f'Move(pos={self._pos}, time={self._timestamp})'

    def __repr__(self) -> str:
        '''Représentation du mouvement.

        Returns:
            str: Représentation du mouvement.
        '''
        return str(self)


    def copy(self) -> 'Move':
        '''Copie le mouvement.

        Returns:
            Move: Copie du mouvement.
        '''
        return Move(self._pos.copy(), timedelta(seconds = self._timestamp.total_seconds()))


    def export(self) -> str:
        '''Exporte le mouvement.

        Returns:
            str: Mouvement exporté.
        '''
        return ';'.join([
            str(self._pos.x) if self._pos is not None else '',
            str(self._pos.y) if self._pos is not None else '',
            str(self._timestamp.total_seconds()),
        ])
