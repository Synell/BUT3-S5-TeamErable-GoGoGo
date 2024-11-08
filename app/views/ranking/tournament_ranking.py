from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from ..decorators import login_required, request_type, RequestType
from .global_ranking import get_top_rank
from ...models import CustomUser

@login_required
@request_type(RequestType.GET)
def tournament_ranking(request: HttpRequest, id_tournament:int) -> HttpResponse:
    '''Controlleur de la page de classement d'un tournois

    Args:
        request (HttpRequest): Requete HTTP
        id_tournament (int): L'id du tournois

    Returns:
        HttpResponse: Reponse HTTP de la page de classement du tournois
    '''
    tournament_users = CustomUser.objects.filter(participatetournament__tournament_id=id_tournament)
    same_ranked = get_top_rank(tournament_users, 1)

    return render(request, 'ranking/tournament-ranking.html', {'user': request.user, 'top_ranked': same_ranked})