from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from ...models import CustomUser, Tournament
from datetime import datetime
from ..decorators import login_required, request_type, RequestType
from ...http import HttpResponseNotifError
from ..code_manager import CodeManager
from .tournament_struct import TournamentStruct
from ..game.game_configuration import create_game_config

def _can_create_tournament(request: HttpRequest) -> bool :
    '''Fonction permettant de savoir s'il est possible de creer un tournoi

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        bool: True si il est possible de creer un tournoi, False sinon
    '''
    current_tournaments = Tournament.objects.filter(creator=request.user, end_date__gt = datetime.now().date()).all()

    can_create = True
    if current_tournaments.count() > 2:
        can_create = False

    return can_create

def _create_tournament_post(request: HttpRequest, tournament_struct: TournamentStruct) -> HttpResponse:
    '''Créer un tournoi à partir des données du formulaire

    Args:
        request (HttpRequest): Requête HTTP
        tournament_struct (TournamentStruct): Le tournoi a créer

    Returns:
        HttpResponse: Réponse HTTP de redirection vers la page du tournoi créé ou erreur
    '''
    private = bool(request.POST.get('tournament-private'))
    ret: HttpResponse = HttpResponseBadRequest('Erreur lors de la création du tournois')
    tournament = construct_tournament(tournament_struct, private, request.user)
    ret = HttpResponse(f'/tournament?id={tournament.id}')
    return ret

@login_required
@request_type(RequestType.GET, RequestType.POST)
def create_tournament(request: HttpRequest) -> HttpResponse:
    '''Créer un tournoi

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Réponse HTTP de redirection vers la page du tournoi créé ou erreur
    '''
    ret: HttpResponse = HttpResponseBadRequest('Erreur lors de la création du tournois')
    if request.method == RequestType.POST.value:
        if (tournament_verif := TournamentStruct.verify_tournament(request)) and isinstance(tournament_verif, Exception):
            ret = HttpResponseNotifError(tournament_verif)
            
        elif _can_create_tournament(request) is False:
            ret = HttpResponseNotifError('Trop de tournois en cours. Attendez la fin de ceux-ci pour en creer un nouveau ou supprimez en un.')

        else:
            ret = _create_tournament_post(request, tournament_verif)

    elif request.method == RequestType.GET.value:
        ret = render(request, 'tournament/create_tournament.html')
    
    return ret


def construct_tournament(tournament_struct: TournamentStruct, private : bool, creator : CustomUser) -> Tournament:
    '''Fonction permettant de construire un tournoi dans la BDD
    
    Args:
        tournament_struct (TournamentStruct): Le tournoi a créer
        private (bool): True si le tournoi est privé, False sinon
        creator (int): L'id de l'utilisateur qui a créé le tournoi

    Returns:
        Tournament: Le tournoi
    '''
    code = CodeManager().generate_tournament_code()
    game_configuration = create_game_config(tournament_struct.game_configuration)
    
    tournament = Tournament.objects.create(
        name = tournament_struct.name,
        description = tournament_struct.description,
        start_date = tournament_struct.start_date,
        private = private,
        end_date = tournament_struct.end_date,
        organisator = tournament_struct.organisator,
        creator = creator,
        register_date = datetime.now().date(),
        code = code,
        player_min = tournament_struct.player_min,
        game_configuration = game_configuration
    )

    return tournament