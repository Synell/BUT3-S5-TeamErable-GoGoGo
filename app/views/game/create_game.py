from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from ...models import Game, GameParticipate, CustomUser
from datetime import datetime
import os, json
from ...logic import Board, RuleFactory, Tile
from ..decorators import login_required, request_type, RequestType
from ...http import HttpResponseNotifError
from ..code_manager import CodeManager
from .game_struct import GameStruct
from .game_configuration import create_game_config
from datetime import timedelta
from ...logic.timer.TimerFactory import TimerFactory
from ...models.game_configuration import GameConfiguration
from ...models.tournament import Tournament
from ...storage import GameStorage

def _create_new_game(request : HttpRequest, game_struct: GameStruct, id_tournament: int) -> HttpRequest:
    '''Fonction permettant de creer une nouvelle partie
    
    Args:
        request (HttpRequest): Requête HTTP
        game_srtuct (GameStruct): La nouvelle partie
        id_tournament (int): L'id du tournoi

    Returns:
        HttpRequest: La requête HTTP
    '''
    partcipate = construct_participate(request.user.id)
    game = construct_game(game_struct, partcipate, id_tournament)

    ret = HttpResponse(f'/game?id={game.id_game}')

    return ret

def construct_participate(id_player1: int, id_player2: int = None) -> GameParticipate:
    '''Fonction permettant de construire un objet GameParticipate dans la BDD
    
    Args:
        id_player1 (int): L'id du premier joueur
        id_player2 (int): L'id du deuxième joueur ou None
    
    Returns:
        GameParticipate: Un objet GameParticipate
    '''
    participate = GameParticipate.objects.create(
        player1 = CustomUser.objects.get(id=id_player1),
        player2 = CustomUser.objects.get(id=id_player2) if id_player2 is not None else None,
        score_player1 = 0,
        score_player2 = 0
    )
    return participate


def create_move_list(game: Game) -> Board:
    '''Fonction permettant de construire le fichir de jeu

    Args:
        game (Game): La nouvelle partie

    Returns:
        Board: Le plateau
    '''
    file = f'dynamic/games/{game.id_game:X}.json'

    if not os.path.exists('dynamic/games'):
        os.makedirs('dynamic/games')

    b = Board(
        int(game.game_configuration.map_size),
        float(game.game_configuration.komi),
        RuleFactory().get(game.game_configuration.counting_method),
        int(game.game_configuration.byo_yomi),
        timedelta(seconds = game.game_configuration.clock_value),
        None,
        TimerFactory().get(game.game_configuration.clock_type),
        None,
    )
    b.place_handicap(game.game_configuration.handicap)
    GameStorage.save_game(file, b)

    game.move_list = file
    game.save()

    return b


def construct_game(game_struct: GameStruct, participate: GameParticipate, id_tournament: int = None) -> Game:
    '''Fonction permettant de construire une nouvelle partie dans la BDD
    
    Args:
        game_struct (GameStruct): La nouvelle partie
        participate (GameParticipate): Les joueurs et les scores de la partie
        id_tournament (int): L'id du tournoi ou None
        
    Returns:
        Game: La nouvelle partie
    '''
    code = CodeManager().generate_game_code()
    game = Game.objects.create(
        name = game_struct.name,
        description = game_struct.description,
        code = code,
        start_date = datetime.now().date(),
        duration = 0,
        done = False,
        tournament = id_tournament,
        game_configuration = create_game_config(game_struct.game_configuration),
        game_participate = participate
    )

    create_move_list(game)

    return game


def construct_game_tournament(name: str, desc: str, game_configuration: GameConfiguration, participate: GameParticipate,tournament: Tournament) -> Game:
    '''Fonction permettant de construire une nouvelle partie dans la BDD
    
    Args:
        name (str): Le nom de la partie
        desc (str): La description de la partie
        game_struct (GameStruct): La nouvelle partie
        participate (GameParticipate): Les joueurs et les scores de la partie
        tournament (Tournament): Le tournoi

        
    Returns:
        Game: La nouvelle partie
    '''
    code = CodeManager().generate_game_code()
    game = Game.objects.create(
        name = name,
        description = desc,
        code = code,
        start_date = datetime.now().date(),
        duration = 0,
        done = False,
        tournament = tournament,
        game_configuration = game_configuration,
        game_participate = participate
    )

    b = create_move_list(game)
    b.pause(Tile.White, True)
    GameStorage.save_game(game.move_list.path, b)

    return game


@login_required
@request_type(RequestType.GET, RequestType.POST)
def create_game(request: HttpRequest, id_tournament: int = None) -> HttpResponse:
    '''Controlleur de la page de création de partie

    Args:
        request (HttpRequest): La requête HTTP
        id_tournament (int): L'id du tournoi ou None

    Returns:
        HttpResponse: La réponse HTTP à la requête de création de partie
    '''
    ret: HttpResponse = HttpResponseNotifError('Erreur lors de la création de la partie')

    if request.method == RequestType.POST.value:

        if (game_verif := GameStruct.verify_game(request)) and isinstance(game_verif, Exception):
            return HttpResponseNotifError(game_verif)

        elif _can_create_game(request) is False:
            ret = HttpResponseNotifError('Trop de parties en cours. Attendez la fin de ceux-ci pour en creer une nouvelle.')
        
        else:
            ret = _create_new_game(request, game_verif, id_tournament)

    elif request.method == RequestType.GET.value:
        ret = render(request, 'game/create_game.html')

    return ret

def _can_create_game(request : HttpRequest) -> bool:
    '''Fonction permettant de savoir si l'utilisateur peut creer une partie
    
    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        bool: True si l'utilisateur peut creer une partie, False sinon
    '''
    current_games = Game.objects.filter(game_participate__in = GameParticipate.objects.filter(player1 = request.user)).filter(done=False).all()

    can_create = False

    if current_games.count() < 5:
        can_create = True
    return can_create