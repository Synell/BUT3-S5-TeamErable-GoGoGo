from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from ...models import CustomUser, Statistic
from ...logic import GoRank
from ..decorators import login_required, request_type, RequestType
from .ranking_struct import RankingStruct
from ..profil.career.career import *

@login_required
@request_type(RequestType.GET)
def global_ranking(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page de classement global

    Args:
        request (HttpRequest): Requete HTTP

    Returns:
        HttpResponse: Reponse HTTP de la page de classement global
    '''
    users = list(CustomUser.objects.all())
    global_ranking = get_top_rank(users, 1)

    friends = list(request.user.friends.all())
    friends.append(request.user)
    friends_ranking = get_top_rank(friends, 1)

    same_ranked_users = list(CustomUser.objects.filter(stat__rank=request.user.stat.rank))
    same_ranked = get_top_rank(same_ranked_users, 1)

    return render(request, 'ranking/global.html', {'user': request.user, 'friends_ranked': friends_ranking, 
        'top_ranked': global_ranking, 'same_ranked': same_ranked})

def get_top_rank(user_range: list[CustomUser], limit:int) -> list[RankingStruct]:
    '''Permet d'obtenir un classement selon une certaine liste d'utilisateurs

        Args:
            user_range (list[CustomUser]): Liste des utilisateurs concernes
            limit (int): position du dernier elment affiche

        Returns:
            list[RankingStruct]: le classement 
    '''
    #Constante correspondant au nombre d'elements du classement affiches simultanement
    LIMIT_RANGE = 20
    ranking:list[CustomUser] = []

    history = {}
    for user in user_range:
        nb_wins = get_total_game_ranked_win(user.id)
        nb_losses = get_total_game_ranked_loose(user.id)
        statistic = Statistic.objects.filter(id=user.stat_id).first()
        history[user] = (nb_wins,nb_wins+nb_losses, statistic)

    ranking = _get_as_ranking(history)
    
    ranking = sorted(ranking, key=_sorting_key, reverse=True)[limit*LIMIT_RANGE-LIMIT_RANGE:limit*LIMIT_RANGE]

    return ranking

def _get_as_ranking(history: dict)-> list[RankingStruct]:
    '''Obtient la liste des structure de ranking pour chaque joueur

        Args:
            history (dict): dictionaire des statistiques de chaque joueurs

        Returns:
            list[RankingStruct]: liste des lignes du classement
    '''

    ranking = []
    for player,player_data in history.items():
        rate = 0
        if(player_data[1]) != 0:
           rate = round(player_data[0]*100/player_data[1], 2)
        ranking.append(RankingStruct(
            player,
            player_data[2].rank,
            player_data[2].elo,
            player_data[1],
            player_data[0],
            player_data[1]-player_data[0],
            rate
        ))

    return ranking

def _sorting_key(ranking_data:RankingStruct)->tuple:
    '''Fonction servant de cle pour la comparaison de tri d'une liste de RankingStruct

        Args:
            ranking_data (RankingStruct): donnes a trier

        Returns:
            tuple: cle de tri
    '''
    rank = GoRank.from_string(ranking_data.rank)
    return (int(rank), ranking_data.taux_victory)