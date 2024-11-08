from enum import Enum
from typing_extensions import Literal

class PauseEnum(Enum):
    '''Pause enum.
    Hérite de Enum'''
    Not = 0
    Normal = 1
    Forced = 2

    def export(self) -> int:
        '''Exporte la valeur.
        
        Returns:
            int: Valeur exportée.
        '''
        return self.value

    def __bool__(self) -> Literal[True]:
        '''Vérifie si la valeur est differente de 0.'''
        return self.value != 0
