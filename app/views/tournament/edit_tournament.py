from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from ...models import Tournament
from datetime import datetime
from ..decorators import login_required, request_type, RequestType
from ...http import HttpResponseNotifError
from .tournament_struct import TournamentStruct
from ..game.game_configuration import edit_game_config


@login_required
@request_type(RequestType.GET, RequestType.POST)
def edit_tournament(request: HttpRequest, id_tournament: int) -> HttpResponse:
    '''Controller de la page de modification d'un tournoi

    Args:
        request (HttpRequest): Requête HTTP
        id_tournament (int): Identifiant du tournoi

    Returns:
        HttpResponse: Réponse HTTP de redirection vers la page du tournoi modifié ou erreur
    '''
    ret: HttpResponse = HttpResponseNotifError('Erreur lors de la modification du tournois')

    if (tournament := can_edit_tournament(id_tournament)) is None:
        ret = HttpResponseRedirect(f'/tournament?id={id_tournament}')

    elif request.method == RequestType.POST.value:
        ret = edit_tournament_post(request, tournament)

    elif request.method == RequestType.GET.value:
        ret = render(request, 'tournament/edit_tournament.html', {'tournament': tournament, 'checked': 'checked' if tournament.private else ''})

    return ret

def modify_tournament(tournament_struct: TournamentStruct, tournament: Tournament, private : bool) -> Tournament:
    '''Fonction permettant de modifier un tournoi dans la BDD

    Args:
        tournament_struct (TournamentStruct): Le tournoi à modifier
        tournament (Tournament): Le tournoi à modifier
        private (bool): True si le tournoi est privé, False sinon

    Returns:
        Tournament: Le tournoi modifié
    '''
    game_configuration = edit_game_config(tournament.game_configuration, tournament_struct.game_configuration)

    tournament.name = tournament_struct.name
    tournament.description = tournament_struct.description
    tournament.start_date = tournament_struct.start_date
    tournament.private = private
    tournament.end_date = tournament_struct.end_date
    tournament.organisator = tournament_struct.organisator
    tournament.register_date = datetime.now().date()
    tournament.player_min = tournament_struct.player_min
    tournament.game_configuration = game_configuration
    tournament.save()

    return tournament

def edit_tournament_post(request: HttpRequest, tournament: Tournament) -> HttpResponse:
    '''Edit le tournoi si le type de requête est POST
    
    Args:
        request (HttpRequest): Requête HTTP
        tournament (Tournament): Le tournoi à modifier

    Returns:
        HttpResponse: Réponse HTTP de redirection vers la page du tournoi modifié ou erreur
    '''
    ret = None

    if (tournament_verif := TournamentStruct.verify_tournament(request)) and isinstance(tournament_verif, Exception):
        return HttpResponseNotifError(tournament_verif)

    private = bool(request.POST.get('tournament-private'))

    try:
        tournament_edited = modify_tournament(tournament_verif, tournament, private)
        ret = HttpResponse(f'/tournament?id={tournament_edited.id}')

    except:
        return HttpResponseNotifError('Erreur lors de la modification du tournois.')

    return ret

def can_edit_tournament(id_tournament: int) -> Tournament:
    '''Fonction permettant de savoir si un tournoi peut être modifié

    Args:
        id_tournament (int): L'id du tournoi

    Returns:
        Tournament: Le tournoi ou None
    '''
    try:
        tournament = Tournament.objects.get(id = id_tournament)
        if datetime.now().date() >= tournament.start_date:
            tournament = None

    except:
        return HttpResponse('/tournament')
    return tournament
