from abc import ABC, abstractmethod
from ..Tile import Tile
from .. import Board
from datetime import timedelta, datetime
from ...exceptions import InvalidMoveException
from .PauseEnum import PauseEnum

class TimerBase(ABC):
    '''Classe abstraite pour le minuteur'''

    key: str = 'base'
    _pause_timer: timedelta = timedelta(minutes = 15)

    def __init__(
        self,
        board: Board,
        byo_yomi: int,
        initial_time: timedelta,
        player_time: dict[Tile, timedelta] | None,
        last_action_time: datetime | None,
        is_paused: PauseEnum = PauseEnum.Not,
        ask_pause: list[Tile] = [],
        ask_resume: list[Tile] = [],
        timer_offset: timedelta = timedelta(seconds = 0),
        date_pause: datetime | None = None,
    ) -> None:
        '''
        Methode du constructeur pour le minuteur

        Args :
            timer_data (dict): Dictionnaire contenant les donnees de configuration du minuteur.
        '''
        self._board = board
        self._byo_yomi = byo_yomi
        self._initial_time = timedelta(seconds = initial_time.total_seconds())
        self._player_time = player_time if player_time is not None else {t: timedelta(seconds = initial_time.total_seconds()) for t in Tile}
        self._last_action_time = last_action_time if last_action_time is not None else datetime.now()
        self._is_paused = is_paused if isinstance(is_paused, PauseEnum) else PauseEnum(is_paused)
        self._ask_pause: list[Tile] = ask_pause.copy()
        self._ask_resume: list[Tile] = ask_resume.copy()
        self._timer_offset: timedelta = timedelta(seconds = timer_offset.total_seconds())
        self._date_pause = datetime.now() if date_pause is None else datetime.fromtimestamp(date_pause.timestamp())


    @property
    def board(self) -> Board:
        '''Plateau de jeu.

        Returns:
            Board: Plateau de jeu.
        '''
        return self._board

    @property
    def byo_yomi(self) -> int:
        '''Periode de byo-yomi.

        Returns:
            int: Periode de byo-yomi.
        '''
        return self._byo_yomi

    @property
    def initial_time(self) -> timedelta:
        '''Temps total.

        Returns:
            timedelta: Temps total.
        '''
        return self._initial_time

    @property
    def player_time(self) -> dict[Tile, timedelta]:
        '''Temps des joueurs.

        Returns:
            timedelta: Temps des joueurs.
        '''
        return self._player_time

    @property
    def last_action_time(self) -> datetime:
        '''Temps du dernier placement.

        Returns:
            datetime: Temps du dernier placement.
        '''
        return self._last_action_time

    @property
    def last_action_time_diff(self) -> timedelta:
        '''Temps depuis le dernier placement.

        Returns:
            timedelta: Temps depuis le dernier placement.
        '''
        if self._is_paused: return self._timer_offset
        return (datetime.now() - self._last_action_time) + self._timer_offset

    @property
    def timed_out(self) -> Tile | None:
        '''Renvoie le joueur qui n'a plus de temps.

        Returns:
            Tile | None: Le joueur qui n'a plus de temps.
        '''
        for t in Tile:
            if self._player_time[t] - self.last_action_time_diff <= timedelta(seconds = 0):
                return t
        return None

    @property
    def is_paused(self) -> PauseEnum:
        '''Indique si le minuteur est en pause.

        Returns:
            PauseEnum: Indique si le minuteur est en pause.
        '''
        return self._is_paused

    @property
    def pause_count(self) -> int:
        '''Nombre de demande de pause.

        Returns:
            int: Nombre de demande de pause.
        '''
        return len(self._ask_pause)

    @property
    def resume_count(self) -> int:
        '''Nombre de demande de reprise.

        Returns:
            int: Nombre de demande de reprise.
        '''
        return len(self._ask_resume)

    @property
    def date_pause(self) -> datetime:
        '''Date de la pause.

        Returns:
            datetime: Date de la pause.
        '''
        return self._date_pause


    @property
    def pause_time_left(self) -> timedelta:
        '''Temps restant avant la reprise.

        Returns:
            timedelta: Temps restant avant la reprise.
        '''
        return max(self._pause_timer - (datetime.now() - self._date_pause), timedelta(seconds = 0))


    @property
    def can_resume(self) -> bool:
        '''Indique si le minuteur peut reprendre.

        Returns:
            bool: True si le minuteur peut reprendre, False sinon.
        '''
        return self._is_paused and (datetime.now() - self._date_pause >= self._pause_timer)


    def update_last_action_time(self) -> None:
        '''Met a jour le temps du dernier placement.'''
        self._last_action_time = datetime.now()


    def reset_timer_offset(self) -> None:
        '''Remet a zero le decalage du minuteur.'''
        self._timer_offset = timedelta(seconds = 0)


    def export(self) -> dict:
        '''Exporte les données du minuteur.

        Returns:
            dict: Données du minuteur.
        '''
        return {
            'key': self.key,
            'byo-yomi': self._byo_yomi,
            'initial-time': self._initial_time.total_seconds(),
            'player-time': {key.value.value: value.total_seconds() for key, value in self._player_time.items()},
            'last-action-time': self._last_action_time.timestamp(),
            'pause': {
                'ask-pause': [t.value.value for t in self._ask_pause],
                'ask-resume': [t.value.value for t in self._ask_resume],
                'is-paused': self._is_paused.export(),
                'timer-offset': self._timer_offset.total_seconds(),
                'date-pause': self._date_pause.timestamp(),
            }
        }


    @abstractmethod
    def copy(self) -> 'TimerBase':
        '''Copie le minuteur.

        Returns:
            TimerBase: Copie du minuteur.
        '''
        pass


    @abstractmethod
    def play(self, tile: Tile) -> timedelta:
        '''Joue un coup.

        Args:
            tile (Tile): Couleur du joueur.

        Returns:
            timedelta: Timestamp du dernier placement.
        '''
        pass


    def add_time(self, tile: Tile, time: timedelta | float | int) -> None:
        '''Ajoute du temps a un joueur.

        Args:
            tile (Tile): Couleur du joueur.
            time (timedelta | float | int): Temps a ajouter.
        '''
        if isinstance(time, timedelta):
            self._player_time[tile] += time
        self._player_time[tile] += timedelta(seconds = time)


    def pause(self, tile: Tile, force: bool = False) -> None:
        '''Met en pause le minuteur.

        Args:
            tile (Tile): Couleur du joueur.
            force (bool, optional): Force la pause. Defaults to False.
        '''
        if self._is_paused: raise InvalidMoveException('Le minuteur est déjà en pause.')
        if tile in self._ask_pause: raise InvalidMoveException('La demande de pause a déjà été faite.')

        if not force: self._ask_pause.append(tile)
        if len(self._ask_pause) == len(Tile) or force:
            self._date_pause = datetime.now()
            self._ask_pause = []
            self._timer_offset = self.last_action_time_diff
            self._is_paused = PauseEnum.Forced if force else PauseEnum.Normal


    def resume(self, tile: Tile) -> None:
        '''Reprend le minuteur.

        Args:
            tile (Tile): Couleur du joueur.
        '''
        if not self._is_paused: raise InvalidMoveException('Le minuteur n\'est pas en pause.')
        if not self.can_resume: raise InvalidMoveException('Le minuteur ne peut pas encore reprendre.')
        if tile in self._ask_resume: raise InvalidMoveException('La demande de reprise a déjà été faite.')

        if self._is_paused == PauseEnum.Forced:
            self._ask_resume.append(tile)
            if len(self._ask_resume) == len(Tile):
                self._ask_pause = []
                self._ask_resume = []
                self.update_last_action_time()
                self._player_time[self._board.current_player] -= self.last_action_time_diff
                self._timer_offset = timedelta(seconds = 0)
                self._is_paused = PauseEnum.Not

        else:
            self._ask_pause = []
            self._ask_resume = []
            self.update_last_action_time()
            self._player_time[self._board.current_player] -= self.last_action_time_diff
            self._timer_offset = timedelta(seconds = 0)
            self._is_paused = PauseEnum.Not
