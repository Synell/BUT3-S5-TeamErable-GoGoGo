from app.translations import Translations

from django.template.defaulttags import register

@register.filter
def translate(key: str) -> str:
    '''Récupère une traduction

    Args:
        key (str): Clé de la traduction

    Returns:
        str: Traduction
    '''
    return Translations.get(key)

Translations.register('japanese', 'Japonais')
Translations.register('chinese', 'Chinois')
