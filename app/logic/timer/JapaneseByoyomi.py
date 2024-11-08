from .TimerBase import TimerBase
from .TimerFactory import TimerFactory
from ...logic import Board, Tile
from datetime import datetime, timedelta
from .PauseEnum import PauseEnum

class JapaneseByoyomi(TimerBase):
	'''Classe de Timer implementant le byo-yomi japonais'''
	key: str = 'japanese'

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
		'''Initialise une timer japonaise.

		Args:
			board (Board): Plateau de jeu.
			byo_yomi (int): Byo-yomi.
			initial_time (timedelta): Duree d'initialisation.
			player_time (dict[Tile, timedelta]): Duree par joueur.
			last_action_time (datetime): Derniere action.
			is_paused (PauseEnum, optional): Pause. Defaults to PauseEnum.Not.
			ask_pause (list[Tile], optional): Demande de pause. Defaults to [].
			ask_resume (list[Tile], optional): Demande de resume. Defaults to [].
			timer_offset (timedelta, optional): Offset. Defaults to timedelta(seconds = 0).
			date_pause (datetime, optional): Date de pause. Defaults to None.
			'''
		super().__init__(board, byo_yomi, initial_time, player_time, last_action_time, is_paused, ask_pause, ask_resume, timer_offset, date_pause)


	def copy(self) -> TimerBase:
		''' Copie de l'objet. '''
		return JapaneseByoyomi(
			self._board,
			self._byo_yomi,
			self._initial_time,
			self._player_time,
			self._last_action_time,
			self._is_paused,
			self._ask_pause,
			self._ask_resume,
			self._timer_offset,
			self._date_pause,
		)


	def play(self, tile: Tile) -> timedelta:
		'''Joue une action.

		Args:
			tile (Tile): Case jouée.
			
		Returns:
			timedelta: Duree restante.
		'''
		delta = datetime.now() - self._last_action_time
		self._player_time[tile] -= delta

		if self._player_time[tile] < timedelta(seconds = self.byo_yomi):
			self._player_time[tile] = timedelta(seconds = self.byo_yomi)

		self.update_last_action_time()
		self.reset_timer_offset()

		return self.initial_time - self._player_time[tile]


TimerFactory().register(JapaneseByoyomi)
