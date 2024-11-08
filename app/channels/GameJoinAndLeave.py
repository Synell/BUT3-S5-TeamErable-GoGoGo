from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from ..models import Game, CustomUser
from ..logic import Board, Tile, Vector2, RankCalculator
from ..exceptions import InvalidMoveException
from ..storage import GameStorage
from ..utils import time2str
from .GameJoinAndLeaveData.end_of_game import end_of_game_callback

class GameJoinAndLeave(WebsocketConsumer):
    '''Gère le websocket de la partie et le jeu.

    Args:
        WebsocketConsumer (_type_): Classe de base du websocket.
    '''

    def connect(self) -> None:
        '''Connecte le joueur à la partie.'''
        self._user = self.scope['user']
        self._game_id = self.scope['url_route']['kwargs']['game_id']

        game = Game.objects.get(id_game = self._game_id)
        self._player_id = 0 if game.game_participate.player1 == self._user else 1 if game.game_participate.player2 == self._user else -1
        if self._player_id == -1: return self.close()

        async_to_sync(self.channel_layer.group_add)(f'game_{self._game_id}', self.channel_name)

        self.accept()


    def receive(self, text_data: str = None, bytes_data: bytes = None) -> None:
        '''Reçoit les décisions du joueur.

        Args:
            text_data (str, optional): Décision du joueur. Défaut à None.
            bytes_data (bytes, optional): Décision du joueur. Défaut à None.

        Raises:
            InvalidMoveException: Une commande non valide a été envoyée.
            InvalidMoveException | ValueError: .
        '''
        try:
            data = json.loads(text_data)
            assert 'type' in data.keys()
            assert 'data' in data.keys()

            match data['type']:
                case 'connect':
                    self.receive_connect(data)

                case 'disconnect':
                    self.receive_disconnect(data)

                case 'play':
                    self.receive_play(data)

                case 'skip':
                    self.receive_skip(data)

                case 'give-up':
                    self.receive_give_up(data)

                case 'check-state':
                    self.receive_check_state(data)

                case 'pause':
                    self.receive_pause(data)

                case 'resume':
                    self.receive_resume(data)

                case 'start':
                    self.receive_start(data)

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
        async_to_sync(self.channel_layer.group_discard)(f'game_{self._game_id}', self.channel_name)
        self.close()


    def _get_game_board(self) -> tuple[Game, Board, Tile]:
        '''Renvoie le jeu, la partie et le joueur.

        Returns:
            tuple[Game, Board, Tile]: Le jeu, la partie et le joueur.
        '''
        game = Game.objects.get(id_game = self._game_id)

        board = GameStorage.load_game(game.move_list.path)

        return game, board, Tile.White if self._player_id == 0 else Tile.Black


    def _end_of_game_callback(self, game: Game, board: Board) -> None:
        '''Met a jour les données liées à la fin de la partie.

        Args:
            game (Game): Partie
            board (Board): Plateau
        '''
        end_of_game_callback(game, board)


    def _update_game(self, game: Game, board: Board) -> None:
        '''Mettre a jour le jeu.
        
        Args:
            game (Game): Le jeu
            board (Board): La partie
        '''
        if board.ended != game.done:
            game.done = board.ended
            game.save()


    def _save_game_board(self, game: Game, board: Board) -> None:
        '''Sauvegarde la partie.

        Args:
            game (Game): Le jeu
            board (Board): La partie
        '''
        self._update_game(game, board)
        GameStorage.save_game(game.move_list.path, board)


    def _get_can_play(self, board: Board) -> int:
        '''Renvoie si le joueur peut jouer.

        Args:
            board (Board): La partie
        
        Returns:
            int: 1 si le joueur peut bouger, 0 sinon, -1 si la partie est finie.
        '''
        current_player = 0 if board.current_player == Tile.White else 1
        current_player = -1 if board.ended else current_player
        return current_player

    def _update_rank_player(self, player: CustomUser) -> CustomUser:
        '''Mets a jour les rangs des joueurs

        Args:
            player (CustomUser): Le joueur

        Returns:
            CustomUser: le joueur avec son nouveau rang
        '''
        total_wins = player.stat.game_ranked_win
        total_losses = player.stat.game_ranked_loose
        total_games = total_wins+total_losses
        rate = 0
        if (total_games != 0):
            rate = total_wins*100/total_games        
        player.stat.rank = RankCalculator.calculate_rank(total_games, rate, 
            player.stat.elo, player.stat.tournament_win)

        return player

    def _update_player_stats(self, game:Game)->None:
        '''Mets a jour les stats des joueurs

        Args:
            game (Game): Le jeu
        '''
        winner = game.game_participate.player1
        loser = game.game_participate.player2
        if(winner != Tile.Black):
            winner = game.game_participate.player2
            loser = game.game_participate.player1

        if game.game_configuration.ranked:
            winner.stat.game_ranked_win += 1
            loser.stat.game_ranked_loose += 1
            winner.stat.elo, loser.stat.elo = RankCalculator.calculate_elo(winner.stat.elo, loser.stat.elo, 32)
        else:
            winner.stat.game_win += 1
            loser.stat.game_loose += 1
            
        winner = self._update_rank_player(winner)
        loser = self._update_rank_player(loser)
        winner.stat.save()
        loser.stat.save()

    def _check_end_game(self, game: Game, board: Board, looser: Tile = None) -> None:
        '''Verifie si la partie est finie et met a jour le jeu.

        Args:
            game (Game): Le jeu
            board (Board): La partie
            looser (Tile, optional): Le joueur qui a perdu. Défaut à None.
        '''
        if board.ended:
            points = board.get_points()

            looser_value = looser.value.color[0] if looser is not None else None

            if looser_value:
                winner = looser.next

            else:
                winner, winner_points = None, 0
                for t in Tile:
                    if points[t] > winner_points: winner, winner_points = t, points[t]


            new_event = {
                'type': 'send_end_game',
                'data': json.dumps({
                    'winner': winner.value.color[0] if winner is not None else None,
                    'looser': looser_value,
                    'points': {
                        t.value.color[0]: {
                            'count': points[t], 'username': game.game_participate.player1.username if t == Tile.White else game.game_participate.player2.username
                        } for t in Tile
                    }
                })
            }

            # Mise a jour des stats joueur
            self._update_player_stats(game)

            # Mise a jour des nombres de parties gagnees/perdues
            
            async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)

            self._end_of_game_callback(game, board)



    def receive_play(self, event: dict) -> None:
        '''Reçoit le coup du joueur.

        Args:
            event (dict): Coup du joueur.

        Raises:
            InvalidMoveException: Le joueur ne peut pas jouer seul.
        '''
        data: str = event['data']

        x, y = data.split(';')
        x = int(x); y = int(y)

        game, board, tile = self._get_game_board()
        if game.game_participate.player2 is None: raise InvalidMoveException('Vous ne pouvez pas jouer seul.')

        ret = board.play(Vector2(x, y), tile)
        parsed_ret = {}
        for key, value in ret.items():
            k = 'r' if not key else key.value.color[0]
            value = [f'{v.x};{v.y}' for v in value]
            parsed_ret[k] = '\n'.join(value)

        self._save_game_board(game, board)

        new_event = {'type': 'send_play', 'data': json.dumps(parsed_ret)}
        async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)

        new_event = {'type': 'send_can_play', 'data': self._get_can_play(board)}
        async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)

        new_event = {'type': 'send_eaten_tiles', 'data': json.dumps({t.value.color[0]: board.get_eaten_tiles(t) for t in Tile})}
        async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)

        game_started = game.game_participate.player2 is not None
        new_event = {'type': 'send_timers', 'data': json.dumps({t.value.color[0]: time2str(v if game_started else board.initial_time) for t, v in board.player_time.items()})}
        async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)

        self._check_end_game(game, board)


    def send_play(self, event: dict) -> None:
        '''Envoie la modification du plateau dû au coup du joueur.

        Args:
            event (dict): Coup du joueur.
        '''
        new_event = {'type': 'play', 'data': event['data']}
        self.send(text_data = json.dumps(new_event))


    def send_can_play(self, event: dict) -> None:
        '''Envoie si le joueur peut jouer.

        Args:
            event (dict): Si le joueur peut jouer.
        '''
        new_event = {'type': 'can-play', 'data': event['data'] == self._player_id}
        self.send(text_data = json.dumps(new_event))


    def send_eaten_tiles(self, event: dict) -> None:
        '''Envoie les pions mangés.

        Args:
            event (dict): Les points du joueur.
        '''
        new_event = {'type': 'eaten-tiles', 'data': event['data']}
        self.send(text_data = json.dumps(new_event))


    def send_timers(self, event: dict) -> None:
        '''Envoie les timers.

        Args:
            event (dict): Les timers.
        '''
        new_event = {'type': 'timers', 'data': event['data']}
        self.send(text_data = json.dumps(new_event))


    def send_end_game(self, event: dict) -> None:
        '''Envoie la fin de la partie.

        Args:
            event (dict): La fin de la partie.
        '''
        new_event = {'type': 'end-game', 'data': event['data']}
        self.send(text_data = json.dumps(new_event))


    def receive_skip(self, event: dict) -> None:
        '''Recoit quand le joueur passe le tour.
        
        Args:
            event (dict): Quand le joueur passe le tour.
            
        Raises:
            InvalidMoveException: Le joueur ne peut pas jouer seul.
        '''
        game, board, tile = self._get_game_board()
        if game.game_participate.player2 is None: raise InvalidMoveException('Vous ne pouvez pas jouer seul.')

        board.play_skip(tile)

        self._save_game_board(game, board)

        new_event = {'type': 'send_can_play', 'data': self._get_can_play(board)}
        async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)

        self._check_end_game(game, board)


    def receive_give_up(self, event: dict) -> None:
        '''Recoit l'abandon du joueur.
        
        Args:
            event (dict): L'abandon du joueur.
            
        Raises:
            InvalidMoveException: Le joueur ne peut pas jouer seul.'''
        game, board, tile = self._get_game_board()
        if game.game_participate.player2 is None: raise InvalidMoveException('Vous ne pouvez pas jouer seul.')

        board.end_game()

        self._save_game_board(game, board)

        new_event = {'type': 'send_can_play', 'data': self._get_can_play(board)}
        async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)

        self._check_end_game(game, board, tile)


    def receive_check_state(self, event: dict) -> None:
        '''Recoit la demande de l'état de la partie.
        
        Args:
            event (dict): La demande de l'état de la partie.
        '''
        game, board, tile = self._get_game_board()

        looser = board.update_game_state()

        if looser:
            GameStorage.save_game(game.move_list.path, board)
            game.done = board.ended
            game.save()

            self._check_end_game(game, board, looser)


    def receive_connect(self, event: dict) -> None:
        '''Reçoit la connexion du joueur.'''
        new_event = {'type': 'send_connect', 'data': {'id': self._user.id, 'color': 'white' if self._player_id == 0 else 'black'}}
        async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)


    def send_connect(self, event: dict) -> None:
        '''Envoie la connexion du joueur.

        Args:
            event (dict): Connexion du joueur.
        '''
        if self._user.id != event['data']['id']:
            new_event = {'type': 'connect', 'data': event['data']}
            self.send(text_data = json.dumps(new_event))


    def receive_disconnect(self, event: dict) -> None:
        '''Reçoit la déconnexion du joueur.

        Args:
            event (dict): Déconnexion du joueur.
        '''
        self.send(text_data = json.dumps(event))


    def receive_pause(self, event: dict) -> None:
        '''Reçoit la demande de pause du joueur.

        Args:
            event (dict): Demande de pause du joueur.

        Raises:
            InvalidMoveException: Le joueur ne peut pas jouer seul.
            InvalidMoveException: Une partie de tournoi ne peut pas être mise en pause.
            InvalidMoveException: Une partie classée ne peut pas être mise en pause.
            InvalidMoveException: Le minuteur est déjà en pause.
        '''
        game, board, tile = self._get_game_board()
        if game.game_participate.player2 is None: raise InvalidMoveException('Vous ne pouvez pas jouer seul.')
        if game.tournament is not None: raise InvalidMoveException('Vous ne pouvez pas mettre en pause une partie de tournoi.')
        if game.game_configuration.ranked: raise InvalidMoveException('Vous ne pouvez pas mettre en pause une partie classée.')
        if board.is_paused: raise InvalidMoveException('Le minuteur est déjà en pause.')

        board.pause(tile)

        self._save_game_board(game, board)

        new_event = {'type': 'send_timers', 'data': json.dumps({t.value.color[0]: time2str(v) for t, v in board.player_time.items()})}
        async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)

        new_event = {'type': 'send_pause', 'data': {'pause_count': board.pause_count, 'is_paused': board.is_paused.value}}
        async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)

        if board.is_paused:
            new_event = {'type': 'send_pause_timer', 'data': {'timer': time2str(board.pause_time_left)}}
            async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)


    def send_pause_timer(self, event: dict) -> None:
        '''Envoie le timer de la pause.

        Args:
            event (dict): Timer de la pause.
        '''
        new_event = {'type': 'pause-timer', 'data': event['data']}
        self.send(text_data = json.dumps(new_event))


    def receive_resume(self, event: dict) -> None:
        '''Reçoit la demande de reprise du joueur.

        Args:
            event (dict): Demande de reprise du joueur.

        Raises:
            InvalidMoveException: Le joueur ne peut pas jouer seul.
            InvalidMoveException: Le minuteur n'est pas en pause.
        '''
        game, board, tile = self._get_game_board()
        if game.game_participate.player2 is None: raise InvalidMoveException('Vous ne pouvez pas jouer seul.')
        if not board.is_paused: raise InvalidMoveException('Le minuteur n\'est pas en pause.')

        board.resume(tile, True)

        self._save_game_board(game, board)

        new_event = {'type': 'send_timers', 'data': json.dumps({t.value.color[0]: time2str(v) for t, v in board.player_time.items()})}
        async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)

        new_event = {'type': 'send_resume', 'data': {'pause_count': board.pause_count, 'is_paused': board.is_paused.value}}
        async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)


    def send_pause(self, event: dict) -> None:
        '''Envoie la demande de pause du joueur.

        Args:
            event (dict): Demande de pause du joueur.
        '''
        new_event = {'type': 'pause', 'data': event['data']}
        self.send(text_data = json.dumps(new_event))


    def send_pause_timer(self, event: dict) -> None:
        '''Envoie le timer de la pause.

        Args:
            event (dict): Timer de la pause.
        '''
        new_event = {'type': 'pause-timer', 'data': event['data']}
        self.send(text_data = json.dumps(new_event))


    def send_resume(self, event: dict) -> None:
        '''Envoie la demande de reprise du joueur.

        Args:
            event (dict): Demande de reprise du joueur.
        '''
        new_event = {'type': 'resume', 'data': event['data']}
        self.send(text_data = json.dumps(new_event))


    def receive_start(self, event: dict) -> None:
        '''Reçoit la demande de début de partie du joueur.

        Args:
            event (dict): Demande de début de partie du joueur.

        Raises:
            InvalidMoveException: Le joueur ne peut pas jouer seul.
            InvalidMoveException: Le minuteur n'est pas en pause.
        '''
        game, board, tile = self._get_game_board()
        if game.game_participate.player2 is None: raise InvalidMoveException('Vous ne pouvez pas jouer seul.')
        if not board.is_paused: raise InvalidMoveException('Le minuteur n\'est pas en pause.')

        board.resume(tile)
        if (not board.is_paused): board.init_start()

        self._save_game_board(game, board)

        new_event = {'type': 'send_timers', 'data': json.dumps({t.value.color[0]: time2str(v) for t, v in board.player_time.items()})}
        async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)

        new_event = {'type': 'send_start', 'data': {'start_count': board.resume_count, 'is_paused': board.is_paused.value}}
        async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)


    def send_start(self, event: dict) -> None:
        '''Envoie la demande de début de partie du joueur.

        Args:
            event (dict): Demande de début de partie du joueur.
        '''
        new_event = {'type': 'start', 'data': event['data']}
        self.send(text_data = json.dumps(new_event))
