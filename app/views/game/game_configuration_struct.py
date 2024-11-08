from dataclasses import dataclass
from ...http import verify_post
from django.http import HttpRequest

@dataclass
class GameConfigurationStruct:
    is_private : bool
    ranked : bool
    map_size : str
    counting_method : str
    byo_yomi : str
    clock_type : str
    time_clock : str
    komi : str
    handicap : str

    @classmethod
    def verify_game_config(cls, request: HttpRequest) -> 'GameConfigurationStruct':
        '''Fonction permettant de valider les informations de la configuration de la partie et de la renvoyer
        
        Args:
            request (HttpRequest): Requête HTTP

        Returns:
            GameConfigurationStruct: La configuration de la partie
        '''
        ret = cls(
            is_private = bool(request.POST.get('game-private')),
            map_size = verify_post(request, 'map-size', 'La taille de la carte est vide.'),
            counting_method = verify_post(request, 'counting-method', 'La methode de comptage est vide.'),
            byo_yomi = verify_post(request, 'byo-yomi', 'Le byo-yomi est vide.'),
            clock_type = verify_post(request, 'clock-type', 'Le temps de la partie est vide.'),
            time_clock = verify_post(request, 'time-clock', 'Le temps de la partie est vide.'),
            komi = verify_post(request, 'komi', 'Le komi est vide.'),
            handicap = verify_post(request, 'handicap', 'Le handicap est vide.'),
            ranked = bool(request.POST.get('game-ranked'))
        )

        return ret
    
    def __str__(self):
        return (f"GameConfigurationStruct(is_private={self.is_private}, "
                f"ranked={self.ranked}, "
                f"map_size={self.map_size}, "
                f"counting_method={self.counting_method}, "
                f"byo_yomi={self.byo_yomi}, "
                f"clock_type={self.clock_type}, "
                f"time_clock={self.time_clock}, "
                f"komi={self.komi}, "
                f"handicap={self.handicap}) ")