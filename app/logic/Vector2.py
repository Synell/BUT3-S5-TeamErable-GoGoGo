class Vector2:
    '''Représente un vecteur à deux dimensions.'''

    def __init__(self, x: int, y: int) -> None:
        '''Constructeur.

        Args:
            x (int): Coordonnée x.
            y (int): Coordonnée y.
        '''
        self._x = x
        self._y = y


    @property
    def x(self) -> int:
        '''Renvoie la coordonnée x.'''
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        '''Modifie la coordonnée x.

        Args:
            value (int): Nouvelle coordonnée x.
        '''
        self._x = value

    @property
    def y(self) -> int:
        '''Renvoie la coordonnée y.'''
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        '''Modifie la coordonnée y.

        Args:
            value (int): Nouvelle coordonnée y.
        '''
        self._y = value


    def __add__(self, other: 'Vector2') -> 'Vector2':
        '''Additionne deux vecteurs.

        Args:
            other (Vector2): Vecteur à additionner.

        Returns:
            Vector2: Vecteur résultant.
        '''
        return Vector2(self._x + other._x, self._y + other._y)

    def __sub__(self, other: 'Vector2') -> 'Vector2':
        '''Soustrait deux vecteurs.

        Args:
            other (Vector2): Vecteur à soustraire.

        Returns:
            Vector2: Vecteur résultant.
        '''
        return Vector2(self._x - other._x, self._y - other._y)

    def __str__(self) -> str:
        '''Surcharge de str.'''
        return f'Vector2({self._x}, {self._y})'

    def __repr__(self) -> str:
        '''Surcharge de repr.'''
        return str(self)

    def __eq__(self, __value: object) -> bool:
        '''Compare deux vecteurs.

        Args:
            __value (object): Vecteur à comparer.

        Returns:
            bool: True si les vecteurs sont égaux, False sinon.
        '''
        if not isinstance(__value, Vector2): return False

        return self._x == __value._x and self._y == __value._y

    def __hash__(self) -> int:
        '''Hash un vecteur.

        Returns:
            int: Hash du vecteur.
        '''
        return hash((self._x, self._y))
    
    def copy(self) -> 'Vector2':
        '''Copie un vecteur.

        Returns:
            Vector2: Copie du vecteur.
        '''
        return Vector2(self._x, self._y)
