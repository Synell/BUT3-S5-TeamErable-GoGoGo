from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from ...http import HttpResponseNotifError
from ...models import ParticipateTournament, Tournament
from datetime import datetime
from django.db.models import Q
from ..decorators import login_required

@login_required
def tournament(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page de tournois
    
    Args:
        request (HttpRequest): Requête HTTP
        
    Returns:
        HttpResponse: La page de tournois
    '''
    return render(request, 'tournament/tournament.html')

def search_tournament(request: HttpRequest) -> HttpResponse:
    '''Recherche les tournois
    
    Args:
        request (HttpRequest): Requête HTTP
        
    Returns:
        HttpResponse: La page avec les tournois
    '''
    ret = None
    if request.method != 'POST':
        ret = HttpResponseBadRequest('')
    else:
        query = request.POST.get('tournament_name','')
        tournaments = Tournament.objects.exclude(id__in = ParticipateTournament.objects.filter(person = request.user).values('tournament')).filter(name__icontains = query).exclude(end_date__lt = datetime.now()).exclude(private = True).order_by('name')[:12]
        ret = render(
            request,
            'reusable/tournament_list.html',
            {'tournaments': tournaments} |
            ({'error': 'Aucun tournoi n\'est disponible pour le moment ou correspond à vos critères de recherche.'} if len(tournaments) == 0 else {})
        )
    return ret

def search_current_tournament(request: HttpRequest) -> HttpResponse:
    '''Recherche les tournois en cours
    
    Args:
        request (HttpRequest): Requête HTTP
        
    Returns:
        HttpResponse: La page des tournois en cours
    '''
    ret = None
    if request.method != 'POST':
        ret = HttpResponseBadRequest('Une erreur est survenue. Veuillez recharger la page pour afficher les tournois.')
    else:
        tournaments = (
            Tournament.objects.filter(Q(id__in = ParticipateTournament.objects.filter(person = request.user).values('tournament')) | Q(creator = request.user)).exclude(end_date__lt = datetime.now()).order_by('name')[:12]
        )
        ret = render(
            request,
            'reusable/tournament_list.html',
            {'tournaments': tournaments} |
            ({'error': 'Vous n\'avez aucun tournoi courant.'} if len(tournaments) == 0 else {})
        )
    return ret

@login_required
def tournament_code(request: HttpRequest) -> HttpResponse:
    '''Cherche les tournois en fonction du code
    
    Args:
        request (HttpRequest): Requête HTTP
        
    Returns:
        HttpResponse: La page du tournois en fonction du code
    '''
    ret = HttpResponseBadRequest('Erreur lors de la recherche du tournoi')
    if (tournament_code := request.POST.get('code')) is None: ret = HttpResponseNotifError('Le code est vide')

    try:
        tournament_inst = Tournament.objects.get(code = tournament_code, end_date__gt = datetime.now())
        if not tournament_inst: ret = HttpResponseNotifError('Aucun tournoi trouvé')
        else:
            ret = HttpResponse(f'/tournament/{tournament_inst.id}/')

    except:
        ret = HttpResponseNotifError('Code invalide')
    return ret
