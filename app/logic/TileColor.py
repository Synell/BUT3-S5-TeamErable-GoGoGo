class TileColor:
    '''Couleur d'une tuile.'''

    def __init__(self, value: str, color: str) -> None:
        '''Initialise une couleur.

        Args:
            value (str): Valeur de la couleur.
            color (str): Couleur de la couleur.
        '''
        self._value = value
        self._color = color

    @property
    def value(self) -> str:
        '''Renvoie la valeur de la couleur.'''
        return self._value

    @property
    def color(self) -> str:
        '''Renvoie la couleur de la couleur.'''
        return self._color

    def __str__(self) -> str:
        '''Surchage de la méthode str'''
        return str(self.value)

    def __repr__(self) -> str:
        '''Surchage de la méthode repr'''
        return self.__str__()
