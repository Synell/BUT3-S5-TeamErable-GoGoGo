from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from ...models.game import Game
from ...models.tournament import Tournament
from ...models.game_participate import GameParticipate
from ...models.game_configuration import GameConfiguration
from datetime import datetime
import random, string, os, json
from ...logic import Board, RuleFactory
from ..decorators import login_required, request_type, RequestType
from ...http import HttpResponseNotifError
from ..code_manager import CodeManager
from ...http import verify_game
from .game_struct import GameStruct
from .game_configuration import create_game_config

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

    file = f'dynamic/games/{game.id_game:X}.json'

    if not os.path.exists('dynamic/games'):
        os.makedirs('dynamic/games')
    with open(file, 'w') as f:
        b = Board(int(game_struct.game_configuration.map_size), float(game_struct.game_configuration.komi), RuleFactory().get(game_struct.game_configuration.counting_method))
        json.dump(b.export(), f)

    game.move_list = file
    game.save()

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
        player1 = id_player1,
        player2 = id_player2,
        score_player1 = 0,
        score_player2 = 0
    )
    return participate

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

    if id_tournament is None:
        configuration = create_game_config(game_struct.game_configuration)
    else:
        configuration = Tournament.objects.get(id_tournament=id_tournament).game_configuration

    game = Game.objects.create(
        name = game_struct.name,
        description = game_struct.description,
        code = code,
        start_date = datetime.now(),
        duration = 0,
        done = False,
        tournament = id_tournament,
        game_configuration = configuration,
        game_participate = participate
    )

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

        if (game_verif := verify_game(request)) and isinstance(game_verif, Exception):
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