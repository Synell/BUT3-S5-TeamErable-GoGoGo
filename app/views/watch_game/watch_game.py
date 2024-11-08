from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from app.models import GameSave
from ...logic import Board, Tile, RuleFactory, TimerFactory
from ..decorators import login_required, request_type, RequestType
from ...utils import time2str
from datetime import timedelta, datetime

@login_required
@request_type(RequestType.GET)
def watch_game(request: HttpRequest) -> HttpResponse:
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
            game_inst = GameSave.objects.get(id_game_save = game_id)
            if not game_inst: raise Exception()
            if not game_inst.user == request.user: raise Exception()

        except:
            return HttpResponseRedirect('/')

        ret = watch_game_view(request, game_inst)

    return ret


def watch_game_view_players(request: HttpRequest, game: GameSave) -> tuple[str, str]:
    '''Logique des joueurs de la partie

    Args:
        request (HttpRequest): Requête HTTP
        game (Game): La partie
        board (Board): Le plateau

    Returns:
        tuple[str, str]: Le HTML des joueurs
    '''

    player1_html = render(
        request,
        'watch_game/watch_game_player.html',
        {
            'player': game.player1,
            'color': Tile.White.value.color,
            'other_color': Tile.Black.value.color,
            'score': 0,
            'timer': time2str(timedelta(seconds = game.clock_value)),
        }
    ).content.decode('utf-8')

    player2_html = render(
        request,
        'watch_game/watch_game_player.html',
        {
            'player': game.player2,
            'color': Tile.Black.value.color,
            'other_color': Tile.White.value.color,
            'score': 0,
            'timer': time2str(timedelta(seconds = game.clock_value)),
        }
    ).content.decode('utf-8')

    return player1_html, player2_html


def watch_game_view(request: HttpRequest, game: GameSave) -> HttpResponse:
    '''Logique de la page de la partie

    Args:
        request (HttpRequest): La requête HTTP
        game (Game): La partie

    Returns:
        HttpResponse: La réponse HTTP à la requête de la partie
    '''

    board = Board(
        game.map_size,
        game.komi,
        RuleFactory().get(game.counting_method),
        game.byo_yomi,
        timedelta(seconds = game.clock_value),
        {
            Tile.White: timedelta(seconds = game.clock_value),
            Tile.Black: timedelta(seconds = game.clock_value),
        },
        TimerFactory().get(game.clock_type),
        datetime.now()
    )

    player1_html, player2_html = watch_game_view_players(
        request,
        game,
    )

    return render(
        request,
        'watch_game/watch_game.html',
        {
            'id': game.id_game_save,
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
            'player1_html': player1_html,
            'player2_html': player2_html,
            'duration': game.duration,
            'duration_formatted': time2str(timedelta(seconds = game.duration)),
            'color': Tile.White.value.color,
        }
    )
