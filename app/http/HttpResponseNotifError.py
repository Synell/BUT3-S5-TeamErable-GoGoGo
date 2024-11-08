from typing import Any
from django.http import HttpResponseBadRequest

class HttpResponseNotifError(HttpResponseBadRequest):
    '''Classe représentant une réponse avec une notification d'erreur'''

    def __init__(self, content: str, *args: Any, **kwargs: Any) -> None:
        '''Constructeur de HttpResponseNotifError

        Args:
            content (str): Contenu de la réponse
            *args (Any): Arguments de position supplémentaires
            **kwargs (Any): Arguments nommés supplémentaires
        '''
        super().__init__(f'<p class="error">{content}<p>', *args, **kwargs)
