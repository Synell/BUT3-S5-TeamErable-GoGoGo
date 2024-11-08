class Player:
    '''Représente un joueur'''

    def __init__(self, id: int) -> None:
        '''Initialise un joueur

        Args:
            id (int): L'id du joueur
        '''
        self._id = id


    @property
    def id(self) -> int:
        '''Renvoie l'id du joueur'''
        return self._id


    def __str__(self) -> str:
        '''Retourne une représentation du joueur sous forme de chaîne de caractères

        Returns:
            str: La représentation du joueur
        '''
        return f'{__class__.__name__}(id = {self._id})'


    def __repr__(self) -> str:
        '''Retourne une représentation du joueur sous forme de chaîne de caractères

        Returns:
            str: La représentation du joueur
        '''
        return str(self)


    def __eq__(self, other: object) -> bool:
        '''Compare deux joueurs

        Args:
            other (object): L'autre joueur

        Returns:
            bool: True si les deux joueurs sont égaux, False sinon
        '''
        return isinstance(other, Player) and self._id == other._id
