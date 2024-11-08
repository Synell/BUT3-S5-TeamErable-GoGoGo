from dataclasses import dataclass
from ...models.custom_user import CustomUser

@dataclass
class RankingStruct:
    '''Structure contenant les statistiques d'un joueur'''
    user : CustomUser
    rank : str
    elo : int
    nb_games : int
    nb_victory : int
    nb_defeats : int
    taux_victory : int

    