from plum import dispatch as overload
from .Vector2 import Vector2
from .Tile import Tile
from .Island import Island
from ..exceptions import InvalidMoveException
from .GoConstants import GoConstants
from .rules import RuleBase, RuleFactory
from .timer import TimerBase, TimerFactory, PauseEnum
from .Grid import Grid
from .Move import Move
from datetime import datetime, timedelta

class Board:
    '''Plateau de jeu.'''

    @overload
    def __init__(self, data: dict) -> None:
        '''Initialise un plateau de jeu.

        Args:
            data (dict): Données du plateau.
        '''
        self.load(data)

    @overload
    def __init__(
        self,
        size: int,
        komi: float,
        rule_cls: type[RuleBase],
        byo_yomi: int,
        time: timedelta,
        player_time: dict[Tile, timedelta] | None,
        timer_cls: type[TimerBase],
        last_action_time: datetime | None,
    ) -> None:
        '''Initialise un plateau de jeu.

        Args:
            size (int): Taille du plateau.
            komi (float): Komi.
            rule_cls (type[RuleBase]): Classe de la règle.
            byo_yomi (int): Byo-yomi.
            time (timedelta): Temps de jeu.
            player_time (dict[Tile, timedelta] | None): Temps de jeu par joueur.
            timer_cls (type[TimerBase]): Classe du timer.
            last_action_time (datetime | None): Dernière action.
        '''
        self._grid = Grid(size)
        self._rule: RuleBase = rule_cls(self, komi)
        self._current_player = Tile.White

        self._eaten_tiles = {}
        for tile in Tile:
            self._eaten_tiles[tile] = 0

        self._ended: bool = False
        self._skip_list: list[Tile] = []
        self._illegal_moves: list[Vector2] = []
        self._history: list[Move] = []

        self._timer = timer_cls(self, byo_yomi, time, player_time, last_action_time)



    @property
    def size(self) -> Vector2:
        '''Renvoi la Taille du plateau.'''
        return self._grid.size

    @property
    def width(self) -> int:
        '''Renvoi la Largeur du plateau.'''
        return self._grid.width

    @property
    def height(self) -> int:
        '''Renvoi la Hauteur du plateau.'''
        return self._grid.height

    @property
    def grid(self) -> Grid:
        '''Renvoi la Grille du plateau de jeu.'''
        return self._grid

    @property
    def raw(self) -> list[list[Tile]]:
        '''Renvoi la Grille du plateau sous forme de liste.'''
        return self._grid.raw

    @property
    def current_player(self) -> Tile:
        '''Renvoi le Joueur courant.'''
        return self._current_player

    @property
    def ended(self) -> bool:
        '''Renvoi True si la partie est terminée. '''
        return self._ended

    @property
    def komi(self) -> float:
        '''Renvoi le Komi. '''
        return self._rule.komi

    @property
    def byo_yomi(self) -> int:
        '''Renvoi le byo-yomi. '''
        return self._timer._byo_yomi

    @property
    def time(self) -> timedelta:
        '''Renvoi le temps. '''
        return self._timer.initial_time

    @property
    def player_time(self) -> dict[Tile, timedelta]:
        '''Renvoi un dictionnaire des temps par joueur. '''
        return (
            {t: v - self._timer.last_action_time_diff for t, v in self._timer.player_time.items() if self.is_player_turn(t)} |
            {t: v for t, v in self._timer.player_time.items() if not self.is_player_turn(t)}
        )

    @property
    def history(self) -> list[Move]:
        '''Renvoi l'historique des actions. '''
        return self._history.copy()

    @property
    def skip_list(self) -> list[Tile]:
        '''Renvoi la liste des joueurs qui ont passé leur tour. '''
        return self._skip_list.copy()

    @property
    def illegal_moves(self) -> list[Vector2]:
        '''Renvoi la liste des coups illegaux. '''
        return self._illegal_moves.copy()

    @property
    def timer(self) -> TimerBase:
        '''Renvoi le timer. '''
        return self._timer

    @property
    def initial_time(self) -> timedelta:
        '''Renvoi le temps initial. '''
        return self._timer.initial_time

    @property
    def is_paused(self) -> PauseEnum:
        '''Renvoi True si le timer est en pause. '''
        return self._timer.is_paused

    @property
    def pause_count(self) -> int:
        '''Renvoi le nombre de demande de pause. '''
        return self._timer.pause_count

    @property
    def resume_count(self) -> int:
        '''Renvoi le nombre de demande de reprise de jeu. '''
        return self._timer.resume_count

    @property
    def can_resume(self) -> bool:
        '''Renvoi True si le timer peut reprendre. '''
        return self._timer.can_resume

    @property
    def pause_time_left(self) -> timedelta:
        '''Renvoi le temps restant avant la reprise'''
        return self._timer.pause_time_left


    def get(self, coords: Vector2) -> Tile:
        '''Renvoie la tuile à la position donnée.

        Args:
            coords (Vector2): Coordonnées.

        Returns:
            Tile: Tuile.
        '''
        return self._grid.get(coords)


    def set(self, coords: Vector2, tile: Tile) -> None:
        '''Modifie la tuile à la position donnée.

        Args:
            coords (Vector2): Coordonnées.
            tile (Tile): Tuile.
        '''
        self._grid.set(coords, tile)


    def is_outside(self, coords: Vector2) -> bool:
        '''Vérifie si les coordonnées sont en dehors du plateau.

        Args:
            coords (Vector2): Coordonnées.

        Returns:
            bool: True si les coordonnées sont en dehors du plateau, False sinon.
        '''
        return self._grid.is_outside(coords)


    def init_start(self) -> None:
        '''Initialise le début de la partie.'''
        self._timer.update_last_action_time()


    def play(self, coords: Vector2, tile: Tile) -> dict[Tile, tuple[Vector2]]:
        '''Joue un coup.

        Args:
            coords (Vector2): Coordonnées du coup.
            tile (Tile): Tuile du joueur.

        Returns:
            dict[Tile, tuple[Vector2]]: Dictionnaire des coups joués.

        Raises:
            InvalidMoveException: Si la partie est terminée.
            InvalidMoveException: Si le temps est en pause.
            InvalidMoveException: Si se n\'est pas le tour du joueur.
            InvalidMoveException: Si le coup est invalide.
            InvalidMoveException: Si les coordonnées sont en dehors du plateau.
            InvalidMoveException: Si la case est déjà occupée.
            InvalidMoveException: Si l'île serait entourée (Si le joueur n'est pas autorisé à jouer dans les zones mortes).
        '''
        if self._ended: raise InvalidMoveException('La partie est terminée.')
        if self._timer.is_paused: raise InvalidMoveException('La partie est en pause.')
        if self._current_player != tile: raise InvalidMoveException('Ce n\'est pas à vous de jouer.')
        if self._grid.is_outside(coords): raise InvalidMoveException('Impossible de jouer ici, les coordonnées sont en dehors du plateau.')
        if self.get(coords) is not None: raise InvalidMoveException('Impossible de jouer ici, la case est déjà occupée.')
        if any(coords == pos for pos in self._illegal_moves): raise InvalidMoveException('Impossible de jouer ici, la case s\'est déjà retrouvée entourée lors du dernier tour.')

        timestamp = self._timer.play(tile)
        if self._timer.timed_out is not None:
            self.end_game()
            return {}

        ret: dict[Tile, list[Vector2]] = {t: [] for t in Tile} | {None: []}

        self.set(coords, tile)

        has_eaten = False

        # Vérifie si le coup mange des pions
        for neightbor in self.get_neighbors(coords):
            if self._grid.is_outside(neightbor): continue

            island = self._grid.get_island_from_coords(neightbor)
            if island is None: continue

            if self._grid.is_island_surronded(island):
                has_eaten = True
                for c in island.coords:
                    self._eaten_tiles[self.get(c).next] += 1
                    self.set(c, None)
                    ret[None].append(c)

        # Si le coup ne mange pas de pions, vérifie si l'île est entourée
        if not has_eaten:
            island = self._grid.get_island_from_coords(coords)
            if self._grid.is_island_surronded(island):
                if GoConstants.AllowPlayInDeadZones:
                    for c in island.coords:
                        self._eaten_tiles[self.get(c)] += 1
                        self.set(c, None)
                        ret[None].append(c)

                else:
                    self.set(coords, None)
                    raise InvalidMoveException('Impossible de jouer ici, l\'île serait entourée.')

        if self.get(coords) is not None:
            ret[tile].append(coords)

        self._history.append(Move(coords, timestamp))
        self._current_player = tile.next
        self._skip_list = []

        # Définie les coups illégaux si un seul pion est mangé
        if len(ret[None]) == 1:
            self._illegal_moves = [ret[None][0]]

        else:
            self._illegal_moves = []

        return ret


    def play_skip(self, tile: Tile) -> None:
        '''Passe le tour.

        Args:
            tile (Tile): Tuile du joueur.

        Raises:
            InvalidMoveException: Si la partie est terminée.
            InvalidMoveException: Si le joueur n'est pas le joueur courant.
            InvalidMoveException: Si le temps est en pause.
        '''
        if self._ended: raise InvalidMoveException('La partie est terminée.')
        if self._timer.is_paused: raise InvalidMoveException('La partie est en pause.')
        if self._current_player != tile: raise InvalidMoveException('Ce n\'est pas à vous de jouer.')

        if self._timer.timed_out is not None:
            self.end_game()
            return
        
        timestamp = self._timer.play(tile)

        self._skip_list.append(tile)

        self._current_player = tile.next
        self._history.append(Move(None, timestamp))
        self._illegal_moves = []

        if set(self._skip_list) == set(Tile):
            self.end_game()


    def pause(self, tile: Tile, force: bool = False) -> None:
        '''Met en pause la partie.

        Args:
            tile (Tile): Tuile du joueur.
            force (bool, optional): Force la pause de la partie. Defaults to False.

        Raises:
            InvalidMoveException: Si la partie est terminée.
        '''
        if self._ended: raise InvalidMoveException('La partie est terminée.')

        self._timer.pause(tile, force)


    def resume(self, tile: Tile) -> None:
        '''Reprend la partie.

        Args:
            tile (Tile): Tuile du joueur.

        Raises:
            InvalidMoveException: Si la partie est terminée.
        '''
        if self._ended: raise InvalidMoveException('La partie est terminée.')

        self._timer.resume(tile)


    def update_game_state(self) -> Tile | None:
        '''Met à jour l'état de la partie.

        Returns:
            Tile | None: Couleur du joueur qui a perdu, None si aucun joueur n'a perdu.
        '''
        ret = None
        if self._timer.timed_out is not None and not self._ended:
            ret = self._timer.timed_out
            self.end_game()

        return ret


    def end_game(self) -> None:
        '''Termine la partie.
        
        Raises:
            InvalidMoveException: Si la partie est terminée.
            InvalidMoveException: Si le temps est en pause.
        '''
        if self._ended: raise InvalidMoveException('La partie est déjà terminée.')
        if self._timer.is_paused: raise InvalidMoveException('La partie est en pause.')
        self._ended = True


    def __str__(self) -> str:
        '''Renvoie le plateau de jeu sous forme de chaine de caractères.'''
        return str(self._grid)

    def __repr__(self) -> str:
        '''Surcharge de l'opérateur str.'''
        return str(self)


    def get_eaten_tiles(self, tile: Tile) -> int:
        '''Renvoie le nombre de tuiles mangées par le joueur.

        Args:
            tile (Tile): Tuile du joueur.

        Returns:
            int: Nombre de tuiles mangées.
        '''
        return self._eaten_tiles[tile]


    def is_player_turn(self, tile: Tile) -> bool:
        '''Vérifie si c'est au joueur de jouer.

        Args:
            tile (Tile): Tuile du joueur.

        Returns:
            bool: True si c'est au joueur de jouer, False sinon.
        '''
        return self._current_player == tile


    def load(self, data: dict) -> None:
        '''Charge un plateau de jeu.

        Args:
            data (dict): Données du plateau.
        '''

        b = data['board']
        size = Vector2(*data.get('size', [len(b[0]), len(b)])[:2])
        self._grid = Grid.from_list([
            [
                Tile.from_value(b[y][x]) if b[y][x] else None
                for x in range(size.x)
            ]
            for y in range(size.y)
        ])
        self._current_player = Tile.from_value(data.get('current-player', Tile.White))
        self._eaten_tiles = {
            Tile.from_value(k): v
            for k, v in data.get('eaten-tiles', {t.value.value: 0 for t in Tile}).items()
        }

        rule_data = data.get('rule', {'key': 'chinese', 'komi': 6.5})
        self._rule = RuleFactory().get(rule_data.get('rule', 'chinese'))(
            self,
            rule_data.get('komi', 6.5),
        )

        self._ended = data.get('ended', False)
        self._skip_list = [Tile.from_value(t) for t in data.get('skip-list', [])]
        self._illegal_moves = [
            Vector2(*pos) if pos else None
            for pos in data.get('illegal-moves', [])
        ]
        history = data.get('history', '')
        self._history = [
            Move(move) for move in history.split('\n')
        ] if history else []

        timer_data = data.get('timer', {
            'key': 'chinese',
            'byo-yomi': 30,
            'initial-time': 3600.0,
            'player-time': {
                Tile.White.value.value: 3600.0,
                Tile.Black.value.value: 3600.0
            },
            'last-action-time': 0.0,
        })
        timer_pause_data = timer_data.get('pause', {
            'ask-pause': [],
            'is-paused': False,
            'timer-offset': 0.0,
        })
        self._timer = TimerFactory().get(timer_data.get('key', 'chinese'))(
            self,
            timer_data.get('byo-yomi', 30),
            timedelta(seconds = timer_data.get('initial-time', 3600)),
            {
                Tile.from_value(k): timedelta(seconds = v) for k, v in timer_data.get('player-time', {}).items()
            },
            datetime.fromtimestamp(timer_data.get('last-action-time', datetime.now().timestamp())),
            timer_pause_data.get('is-paused', False),
            [Tile.from_value(t) for t in timer_pause_data.get('ask-pause', [])],
            [Tile.from_value(t) for t in timer_pause_data.get('ask-resume', [])],
            timedelta(seconds = timer_pause_data.get('timer-offset', 0.0)),
            datetime.fromtimestamp(timer_pause_data.get('date-pause', datetime.now().timestamp())),
        )


    def export(self) -> dict:
        '''Exporte le plateau de jeu.

        Returns:
            dict: Données du plateau.
        '''
        return {
            'board': [
                [
                    str(self.get(Vector2(x, y))) if self.get(Vector2(x, y)) else None
                    for x in range(self.size.x)
                ]
                for y in range(self.size.y)
            ],
            'size': [self.size.x, self.size.y],
            'current-player': str(self._current_player),
            'eaten-tiles': {
                str(tile): self._eaten_tiles[tile]
                for tile in Tile
            },
            'rule': self._rule.export(),
            'ended': self._ended,
            'skip-list': [str(tile) for tile in self._skip_list],
            'illegal-moves': [[pos.x, pos.y] if pos else None for pos in self._illegal_moves],
            'history': '\n'.join([move.export() for move in self._history]),
            'timer': self._timer.export(),
        }


    def copy(self) -> 'Board':
        '''Copie le plateau de jeu.

        Returns:
            Board: Copie du plateau de jeu.
        '''
        b = Board(
            self.size.x,
            self.komi,
            self._rule.__class__,
            self.byo_yomi,
            timedelta(seconds = self.time.total_seconds()),
            {k: timedelta(seconds = v.total_seconds()) for k, v in self.player_time.items()},
            self._timer.__class__,
            datetime.fromtimestamp(self._timer.last_action_time.timestamp()) if self._timer.last_action_time is not None else None,
        )
        b._grid = Grid.from_list([row.copy() for row in self._grid])
        b._current_player = self._current_player
        b._eaten_tiles = self._eaten_tiles.copy()
        b._ended = self._ended
        b._skip_list = self._skip_list.copy()
        b._illegal_moves = [pos.copy() for pos in self._illegal_moves]
        b._history = [move.copy() for move in self._history]

        return b


    def get_false_eyes(self) -> list[Vector2]:
        '''Renvoie les positions des yeux faux.

        Returns:
            list[Vector2]: Positions des yeux faux.
        '''
        return self._grid.get_false_eyes()
    

    def get_territories(self) -> dict[Tile, list[Island]]:
        '''Renvoie les territoires.

        Returns:
            dict[Tile, list[Island]]: Territoires.
        '''
        return self._grid.get_territories()


    def get_neighbors(self, coords: Vector2) -> list[Vector2]:
        '''Renvoie les voisins d'une case.

        Args:
            coords (Vector2): Coordonnées.

        Returns:
            list[Vector2]: Voisins.
        '''
        return self._grid.get_neighbors(coords)


    def get_points(self) -> dict[Tile, float]:
        '''Renvoie les points des joueurs.

        Returns:
            dict[Tile, float]: Points.
        '''
        return self._rule.count_points()


    def place_handicap(self, handicap: int) -> None:
        '''Place les pierres de handicap.

        Args:
            handicap (int): Nombre de pierres de handicap.

        Raises:
            InvalidMoveException: Le nombre de pierres de handicap n'est pas supporté pour cette taille de plateau.
        '''
        if not handicap: return

        for k in GoConstants.HandicapStones.keys():
            if k == self.size.x:
                for coords in GoConstants.HandicapStones[k][:handicap]:
                    self.set(coords, Tile.Black)

                return
            
        raise InvalidMoveException('Le nombre de pierres de handicap n\'est pas supporté pour cette taille de plateau.')
