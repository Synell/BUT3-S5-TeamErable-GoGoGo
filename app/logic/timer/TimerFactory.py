from .TimerBase import TimerBase
from ...utils import Singleton

class TimerFactory(metaclass = Singleton):
    '''Fabrique de timer. Serve de singleton.'''

    def __init__(self) -> None:
        '''Initialise la fabrique de timer.'''
        self._timers = {}

    def register(self, timer_cls: type[TimerBase]) -> None:
        '''Enregistre un timer.

        Args:
            timer_cls (type[TimerBase]): Classe du timer.
        '''
        self._timers[timer_cls.key] = timer_cls

    def get(self, key: str) -> type[TimerBase]:
        '''Renvoie un timer.

        Args:
            key (str): Clé du timer.

        Returns:
            type[TimerBase]: Classe du timer.
        '''
        return self._timers[key]
