from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from ...models import Tournament
from ...http import HttpResponseNotifError
from datetime import datetime
from ..decorators import login_required

@login_required
def delete_tournament(request: HttpRequest, id_tournament: int) -> HttpResponse:
    '''Fonction permettant de supprimer un tournoi
    
    Args:
        request (HttpRequest): Requête HTTP
        id_tournament (int): L'id du tournoi a supprimer
        
    Returns:
        HttpResponse: La page de la liste des tournois ou erreur
    '''
    ret: HttpResponse = HttpResponseBadRequest('Erreur lors de la suppression du tournoi')

    try:
        tournament = Tournament.objects.get(id=id_tournament)
        
        if tournament.creator.id == request.user.id and tournament.start_date >= datetime.now().date():
            configuration = tournament.game_configuration
            tournament.delete()
            configuration.delete()
            ret = HttpResponseRedirect('/tournament')

        else:
            ret = HttpResponseNotifError('Vous ne pouvez pas supprimer ce tournoi')

    except:
        return HttpResponseNotifError('Erreur lors de la suppression du tournois')

    return ret