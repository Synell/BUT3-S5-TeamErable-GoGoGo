from enum import Enum, auto

class GoRank(Enum):
    '''Classe des rangs de Go.'''
    _30_Kyu = auto()
    _29_Kyu = auto()
    _28_Kyu = auto()
    _27_Kyu = auto()
    _26_Kyu = auto()
    _25_Kyu = auto()
    _24_Kyu = auto()
    _23_Kyu = auto()
    _22_Kyu = auto()
    _21_Kyu = auto()
    _20_Kyu = auto()
    _19_Kyu = auto()
    _18_Kyu = auto()
    _17_Kyu = auto()
    _16_Kyu = auto()
    _15_Kyu = auto()
    _14_Kyu = auto()
    _13_Kyu = auto()
    _12_Kyu = auto()
    _11_Kyu = auto()
    _10_Kyu = auto()
    _9_Kyu = auto()
    _8_Kyu = auto()
    _7_Kyu = auto()
    _6_Kyu = auto()
    _5_Kyu = auto()
    _4_Kyu = auto()
    _3_Kyu = auto()
    _2_Kyu = auto()
    _1_Kyu = auto()

    _1_Dan = auto()
    _2_Dan = auto()
    _3_Dan = auto()
    _4_Dan = auto()
    _5_Dan = auto()
    _6_Dan = auto()
    _7_Dan = auto()
    _8_Dan = auto()
    _9_Dan = auto()

    @classmethod
    def from_string(cls, rank_str : str) -> 'GoRank':
        '''Renvoie un rang depuis une chaîne de caractères.

        Args:
            cls (GoRank): Classe.
            rank_str (str): Nom du rang.

        Returns:
            GoRank: Rang.
        '''
        if('ème ' in rank_str):
            rank_number, rank_type = rank_str.split('ème ')
        else:
            rank_number, rank_type = rank_str.split('er ')
        rank_number = int(rank_number)

        return cls[f'_{rank_number}_{rank_type}']

    def __str__(self):
        '''Surcharge de l'opérateur str.'''
        rank_number = self.name.split('_')[1]
        suffix = "ème"
        if rank_number == str(1):
            suffix = "er"
        if 'Kyu' in self.name:
            return f"{rank_number}{suffix} Kyu"
        elif 'Dan' in self.name:
            return f"{rank_number}{suffix} Dan"

    def __int__(self):
        '''Constructeur.'''
        return self.value