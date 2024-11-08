from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from ..models import GameSave
from ..logic import Board, Tile, Vector2, RuleFactory, TimerFactory
from ..exceptions import InvalidMoveException
from .WatchGameJoinAndLeaveData.WatchMove import WatchMove
from datetime import timedelta, datetime
from typing import Any
from math import floor


class WatchGameJoinAndLeave(WebsocketConsumer):
    '''Gère le websocket de la partie et le jeu.

    Args:
        WebsocketConsumer (_type_): Classe de base du websocket.
    '''

    def connect(self) -> None:
        '''Connecte le joueur à la partie.'''
        self._user = self.scope['user']
        self._game_id = self.scope['url_route']['kwargs']['game_id']
        self._game_save = GameSave.objects.get(id_game_save = self._game_id)

        if self._user != self._game_save.user:
            return self.close()

        board = Board(
            self._game_save.map_size,
            self._game_save.komi,
            RuleFactory().get(self._game_save.counting_method),
            self._game_save.byo_yomi,
            timedelta(seconds = self._game_save.clock_value),
            {
                Tile.White: timedelta(seconds = self._game_save.clock_value),
                Tile.Black: timedelta(seconds = self._game_save.clock_value),
            },
            TimerFactory().get(self._game_save.clock_type),
            datetime.now()
        )

        self._moves: list[WatchMove] = []

        move_list = self._game_save.move_list.split('\n')
        timestamps_tmp = {t: [] for t in Tile}
        for i, m in enumerate(move_list):
            t = timedelta(seconds = float(m.split(';')[2]))
            if i % 2 == 0: timestamps_tmp[Tile.White].append(t)
            else: timestamps_tmp[Tile.Black].append(t)

        after_durations = {t: [] for t in Tile}
        for t in Tile:
            for e in timestamps_tmp[t]:
                after_durations[t].append(timedelta(seconds = e.total_seconds()))

        for t in Tile: timestamps_tmp[t].insert(0, timedelta(seconds = 0))

        durations = {t: [] for t in Tile}
        for t in Tile:
            while len(timestamps_tmp[t]) > 1:
                el = timestamps_tmp[t].pop(0)
                durations[t].append(timestamps_tmp[t][0] - el)

        duraction_list = []
        index = 0
        while durations[Tile.White] or durations[Tile.Black]:
            if index % 2 == 0:
                duraction_list.append(durations[Tile.White].pop(0))

            else:
                duraction_list.append(durations[Tile.Black].pop(0))

            index += 1

        if durations[Tile.White]: duraction_list.append(durations[Tile.White].pop(0))

        total_time = timedelta(seconds = 0)

        for i, move in enumerate(move_list):
            if move == '': continue

            x, y, _ = move.split(';')
            current_player = board.current_player
            if x == '' and y == '':
                board.play_skip(current_player)
                changes = {}

            else:
                changes = board.play(Vector2(int(float(x)), int(float(y))), current_player)

            time = duraction_list.pop(0)
            self._moves.append(
                WatchMove(
                    total_time,
                    total_time + time,
                    current_player,
                    after_durations[current_player].pop(0),
                    {t: board.get_eaten_tiles(t) for t in Tile},
                    changes
                )
            )
            total_time += time

        async_to_sync(self.channel_layer.group_add)(f'gamesave_{self._game_id}', self.channel_name)

        self.accept()


    def receive(self, text_data: str = None, bytes_data: bytes = None) -> None:
        '''Reçoit les décisions du joueur.

        Args:
            text_data (str, optional): Décision du joueur. Défaut à None.
            bytes_data (bytes, optional): Décision du joueur. Défaut à None.

        Raises:
            InvalidMoveException: Exception lorsqu'une partie est invalide.
            ValueError: Une commande non valide a été envoyée.
        '''
        try:
            data = json.loads(text_data)
            assert 'type' in data.keys()
            assert 'data' in data.keys()

            match data['type']:
                case 'get':
                    self._receive_get(data['data'])

                case _:
                    raise ValueError('Une commande non valide a été envoyée.')

        except (InvalidMoveException, ValueError) as e:
            self.send(text_data = json.dumps({'type': 'error', 'data': str(e)}))

        except Exception as e:
            pass


    def disconnect(self, code: int) -> None:
        '''Enlève le joueur de la salle s'il n'est plus connecté.
        
        Args:
            code (int): Code de l'erreur.
        '''
        async_to_sync(self.channel_layer.group_discard)(f'gamesave_{self._game_id}', self.channel_name)
        self.close()


    def _get_index_of(self, list_: list, value: Any) -> int:
        '''Retourne l'index d'une valeur dans une liste.

        Args:
            list_ (list): Liste.
            value (any): Valeur.

        Returns:
            int: Index de la valeur.
        '''
        for i, v in enumerate(list_):
            if v == value: return i

        return -1


    def _merge_moves(self, moves: list[WatchMove]) -> dict[Tile, list[Vector2]]:
        '''Fusionne les changements de plusieurs mouvements.

        Args:
            moves (list[WatchMove]): Liste des mouvements.

        Returns:
            dict[Tile, list[Vector2]]: Changements fusionnés.
        '''
        changes: dict[Tile, list[Vector2]] = {None: []} | {t: [] for t in Tile}

        for move in moves:
            for v in move.changes[None]:
                for t in Tile:
                    index = self._get_index_of(changes[t], v)
                    if index != -1: changes[t].pop(index)

                changes[None].append(v)

            for t in Tile:
                for v in move.changes[t]:
                    index = self._get_index_of(changes[None], v)
                    if index != -1: changes[None].pop(index)

                    changes[t].append(v)

        return changes


    def _get_changes(self, from_: timedelta, to_: timedelta) -> tuple[dict[Tile, tuple[Vector2]], dict[Tile, timedelta], dict[Tile, int]]:
        '''Retourne les changements entre deux timestamps.

        Args:
            from_ (timedelta): Timestamp de début.
            to_ (timedelta): Timestamp de fin.

        Returns:
            tuple[dict[Tile, tuple[Vector2]], list[timedelta], dict[Tile, int]]: Changements, temps des joueurs, tuiles mangées.
        '''
        invert = False
        if from_ < timedelta(seconds = 0) or to_ < timedelta(seconds = 0):
            return {None: [Vector2(x, y) for x in range(self._game_save.map_size) for y in range(self._game_save.map_size)]} | {t: [] for t in Tile}

        if from_ > to_:
            ret = {None: [Vector2(x, y) for x in range(self._game_save.map_size) for y in range(self._game_save.map_size)]} | {t: [] for t in Tile}
            invert = True
            from_ = timedelta(seconds = 0)

        from_index = [i for i, move in enumerate(self._moves) if move.time_overlap(from_)]
        to_index = [i for i, move in enumerate(self._moves) if move.time_overlap(to_)]

        if not from_index: return self._get_changes(from_ - timedelta(seconds = 1), to_)
        elif not to_index: return self._get_changes(from_, to_ - timedelta(seconds = 1))
        from_index = from_index[0]
        to_index = to_index[-1]

        moves = self._moves[from_index:to_index + 1]

        changes: dict[Tile, list[Vector2]] = self._merge_moves(moves)
        if invert:
            for t in Tile:
                for v in changes[t]:
                    index = self._get_index_of(ret[None], v)
                    if index != -1: ret[None].pop(index)

        else: ret = changes

        times = []
        eaten_tiles = {}

        if moves:
            times.append(moves[-1].player_time)
            index = to_index - 1

            if moves[-1].player == Tile.White:
                if index > -1: times.append(self._moves[index].player_time)
                else: times.append(timedelta(seconds = 0))

            else:
                if index > -1: times.insert(0, self._moves[index].player_time)
                else: times.insert(0, timedelta(seconds = 0))

            eaten_tiles = moves[-1].eaten_tiles

        else:
            times = [timedelta(seconds = 0), timedelta(seconds = 0)]
            eaten_tiles = {t: 0 for t in Tile}

        return {t: tuple(v) for t, v in ret.items()}, {Tile.White: times[0], Tile.Black: times[1]}, eaten_tiles


    def _changes_to_json(self, changes: dict[Tile, tuple[Vector2]]) -> dict:
        '''Convertit les changements en json.

        Args:
            changes (dict[Tile, tuple[Vector2]]): Changements.

        Returns:
            str: Changements en json.
        '''
        return {
            t.value.color[0] if t else 'r': '\n'.join([
                f'{vec.x};{vec.y}'
                for vec in v
            ])
            for t, v in changes.items()
        }


    def _receive_get(self, data: dict) -> None:
        '''Reçoit une demande de données.

        Args:
            data (dict): Données.

        Raises:
            ValueError: Les données ne sont pas valides.
        '''
        if 'from' not in data.keys() or 'to' not in data.keys():
            raise ValueError('Les données envoyées ne sont pas valides.')

        from_ = timedelta(seconds = data['from'])
        to_ = timedelta(seconds = data['to'])

        changes, timers, eaten_tiles = self._get_changes(from_, to_)
        changes_json = self._changes_to_json(changes)

        self.send(text_data = json.dumps({ 'type': 'changes', 'data': changes_json }))
        self.send(text_data = json.dumps({ 'type': 'timers', 'data': { t.value.color[0]: self._game_save.clock_value - floor(timers[t].total_seconds()) for t in Tile } }))
        self.send(text_data = json.dumps({ 'type': 'eaten-tiles', 'data': { 'r' if not t else t.value.color[0]: eaten_tiles[t] for t in Tile } }))
