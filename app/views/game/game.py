from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from app.models import Game
from ...logic import Board, Tile
from ..decorators import login_required, request_type, RequestType
from ...http import HttpResponseNotifError
from ...storage import GameStorage
from ...models import CustomUser
from ...utils import time2str
from datetime import timedelta

@login_required
@request_type(RequestType.GET)
def game(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page de la partie

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Réponse HTTP à la requête de la partie
    '''
    ret: HttpResponse = HttpResponseBadRequest()

    if (game_id := request.GET.get('id')) is None: ret = HttpResponseRedirect('/')

    else:
        try:
            game_inst = Game.objects.get(id_game = game_id, done = False)
            if not game_inst: ret = HttpResponseRedirect('/')

        except:
            return HttpResponseRedirect('/')

        if game_inst.game_participate.player1 != request.user and game_inst.game_participate.player2 is None and not game_inst.game_configuration.is_private:
            game_inst.game_participate.player2 = request.user
            game_inst.game_participate.save()

            board = GameStorage.load_game(game_inst.move_list.path)
            board.init_start()
            GameStorage.save_game(game_inst.move_list.path, board)

        if game_inst.game_participate.player1 != request.user and game_inst.game_participate.player2 != request.user: return HttpResponseRedirect('/')

        ret = game_view(request, game_inst)

    return ret


@login_required
@request_type(RequestType.POST)
def game_code(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page de la partie via code

    Args:
        request (HttpRequest): La requête HTTP

    Returns:
        HttpResponse: La réponse HTTP à la requête de la partie
    '''
    ret: HttpResponse = HttpResponseBadRequest()

    if (game_code := request.POST.get('code')) is None: ret = HttpResponseNotifError('Le code est vide.')

    else:
        try:
            game_inst = Game.objects.get(code = game_code, done = False)
            if not game_inst: return HttpResponseNotifError('Aucune partie avec ce code.')

        except:
            return HttpResponseNotifError('Une erreur est survenue. Veuillez réessayer.')

        if game_inst.game_participate.player1 != request.user and game_inst.game_participate.player2 is None:
            game_inst.game_participate.player2 = request.user
            game_inst.game_participate.save()

            board = GameStorage.load_game(game_inst.move_list.path)
            board.init_start()
            GameStorage.save_game(game_inst.move_list.path, board)

        if game_inst.game_participate.player1 != request.user and game_inst.game_participate.player2 != request.user: return HttpResponseNotifError('Vous n\'êtes pas autorisé à rejoindre la partie.')

        ret = HttpResponse(f'/game?id={game_inst.id_game}')

    return ret


def game_view_players(request: HttpRequest, game: Game, board: Board, players: list[CustomUser]) -> tuple[str, str]:
    '''Logique des joueurs de la partie

    Args:
        request (HttpRequest): Requête HTTP
        game (Game): La partie
        board (Board): Le plateau
        players (list[CustomUser]): La liste des joueurs

    Returns:
        tuple[str, str]: Le HTML des joueurs
    '''

    player1, player2 = players

    player1_color = Tile.White if player1 == game.game_participate.player1 else Tile.Black
    player2_color = Tile.White if player2 == game.game_participate.player1 else Tile.Black

    game_started = game.game_participate.player2 is not None

    player1_html = render(
        request,
        'reusable/game_player.html',
        {
            'player': player1,
            'color': player1_color.value.color,
            'other_color': player2_color.value.color,
            'score': board.get_eaten_tiles(player1_color),
            'timer': time2str(board.player_time[player1_color] if game_started else board.initial_time),
        }
    ).content.decode('utf-8')

    player2_html = render(
        request,
        'reusable/game_player.html',
        {
            'player': player2,
            'color': player2_color.value.color,
            'other_color': player1_color.value.color,
            'score': board.get_eaten_tiles(player2_color),
            'timer': time2str(board.player_time[player2_color] if game_started else board.initial_time),
        }
    ).content.decode('utf-8')

    return player1_html, player2_html


def game_view(request: HttpRequest, game: Game) -> HttpResponse:
    '''Logique de la page de la partie

    Args:
        request (HttpRequest): La requête HTTP
        game (Game): La partie

    Returns:
        HttpResponse: La réponse HTTP à la requête de la partie
    '''
    board = GameStorage.load_game(game.move_list.path)
    tile = Tile.White if request.user == game.game_participate.player1 else Tile.Black
    can_play = board.is_player_turn(tile)
    players = [game.game_participate.player1, game.game_participate.player2]

    player1_html, player2_html = game_view_players(
        request,
        game,
        board,
        [
            request.user,
            players[1] if players[0] == request.user else players[0]
        ]
    )

    color = Tile.White if request.user == game.game_participate.player1 else Tile.Black
    has_second_player = game.game_participate.player2 is not None

    return render(
        request,
        'game/game.html',
        {
            'id': game.id_game,
            'color': color.value.color,
            'has_second_player': has_second_player,
            'game_ended': board.ended,
            'board': [
                [
                    {
                        'tile': tile if tile else '',
                        'x': x,
                        'y': y,
                    }
                    for x, tile in enumerate(row)
                ]
                for y, row in enumerate(board.raw)
            ],
            'can_play': 'can-play' * int(can_play and not board.ended),
            'player1_html': player1_html,
            'player2_html': player2_html,
            'code': game.code,
            'action_buttons_class': '' if can_play and not board.ended else 'hidden',
            'game_paused': board.is_paused.value,
            'pause_count': board.pause_count,
            'start_count': board.resume_count,
            'resume_timer': time2str(board.pause_time_left),
            'hide_pause': game.game_configuration.ranked or (game.tournament is not None),
        }
    )

@login_required
@request_type(RequestType.POST)
def game_view_player(request: HttpRequest) -> HttpResponse:
    '''Logique pour récupérer le HTML d'un joueur

    Args:
        request (HttpRequest): La requête HTTP

    Raises:
        Exception: Le joueur ou la partie n'existe pas
        Exception: Le joueur n'est pas dans la partie

    Returns:
        HttpResponse: Le HTML du joueur
    '''
    ret: HttpResponse = HttpResponseBadRequest()

    if ((game_id := request.POST.get('game-id')) is not None) and ((player := request.POST.get('user-id')) is not None):
        try:
            game_inst = Game.objects.get(id_game = game_id, done = False)
            user_inst = CustomUser.objects.get(id = player)

            if (not game_inst) or (not user_inst): raise Exception('La partie ou le joueur n\'existe pas.')
            if game_inst.game_participate.player1 != request.user and game_inst.game_participate.player2 != request.user: raise Exception('Vous n\'êtes pas dans la partie.')

        except Exception as e:
            return HttpResponseBadRequest(str(e))

        board = GameStorage.load_game(game_inst.move_list.path)

        player1_html, player2_html = game_view_players(
            request,
            game_inst,
            board,
            [game_inst.game_participate.player1, game_inst.game_participate.player2]
        )

        ret = HttpResponse(player1_html if user_inst == game_inst.game_participate.player1 else player2_html)

    return ret
