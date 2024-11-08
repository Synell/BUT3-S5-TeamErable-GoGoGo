from ...models import Game, GameSave
from ...logic import Board, Tile
from ...views.tournament.tournament_game import update_tournament_games
from ...storage import TournamentStorage, GameStorage
from ...tournament_logic import Player
from math import ceil


def _update_tournament_data(game: Game, board: Board) -> None:
    '''Met a jour les données liées à la fin de la partie d'un tournoi.
    
    Args:
        game (Game): Partie
        board (Board): Plateau
    '''
    if game.tournament is not None:
        tournament_logic = TournamentStorage.load_tournament(game.tournament.tournament_status.path)
        points = board.get_points()
        winner = game.game_participate.player1 if points[Tile.White] > points[Tile.Black] else game.game_participate.player2
        tournament_logic.do_win(Player(winner.id))
        TournamentStorage.save_tournament(game.tournament.tournament_status.path, tournament_logic)
        update_tournament_games(game.tournament)


def _delete_game(game: Game) -> None:
    '''Supprime une partie

    Args:
        game (Game): Partie
    '''
    path = game.move_list.path
    GameStorage.delete_game(path)
    game.delete()


def _convert_game_to_game_save(game: Game, board: Board) -> None:
    '''Convertit une partie en partie sauvegardée

    Args:
        game (Game): Partie
        board (Board): Plateau
    '''
    try:
        players = (game.game_participate.player1, game.game_participate.player2)
        points = board.get_points()
        for player in players:
            old_game_saves = GameSave.objects.filter(user = player).order_by('-id_game_save')[49:]
            for old_game_save in old_game_saves:
                old_game_save.delete()

            GameSave.objects.create(
                user = player,
                name = game.name,
                player1 = game.game_participate.player1,
                player2 = game.game_participate.player2,
                score_player1 = points[Tile.White],
                score_player2 = points[Tile.Black],
                duration = ceil(((board.time - board.player_time[Tile.White]) + (board.time - board.player_time[Tile.Black])).total_seconds()),
                move_list = '\n'.join([move.export() for move in board._history]),
                tournament = game.tournament,
                map_size = game.game_configuration.map_size,
                komi = game.game_configuration.komi,
                counting_method = game.game_configuration.counting_method,
                clock_type = game.game_configuration.clock_type,
                clock_value = game.game_configuration.clock_value,
                byo_yomi = game.game_configuration.byo_yomi,
                handicap = game.game_configuration.handicap,
            )

        _delete_game(game)

    except Exception as e: pass


def end_of_game_callback(game: Game, board: Board) -> None:
    '''Met a jour les données liées à la fin de la partie.

    Args:
        game (Game): Partie
        board (Board): Plateau
    '''
    _update_tournament_data(game, board)
    _convert_game_to_game_save(game, board)
