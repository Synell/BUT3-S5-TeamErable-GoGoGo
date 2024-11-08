class Translations:
    '''Classe de traduction'''

    _translations: dict = {}

    def __new__(cls) -> None:
        '''Empêche l'instanciation de la classe'''
        return None

    @staticmethod
    def register(key: str, translation: str) -> None:
        '''Enregistre une traduction

        Args:
            key (str): Clé de la traduction
            translation (str): Traduction
        '''
        Translations._translations[key] = translation

    @staticmethod
    def get(key: str) -> str:
        '''Récupère une traduction

        Args:
            key (str): Clé de la traduction

        Returns:
            str: Traduction
        '''
        return Translations._translations[key]

    @staticmethod
    def get_all() -> dict[str, str]:
        '''Récupère toutes les traductions

        Returns:
            dict[str, str]: Traductions
        '''
        return Translations._translations.copy()
