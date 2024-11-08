from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from app.models import CustomUser, Game, Tournament, ParticipateTournament
from ..decorators import login_required
from ...http import HttpResponseNotifError
from ...tournament_logic import Tournament as TournamentLogic, IMatch, Bracket, Match, Player
from .tournament_game import start_tournament
from ...storage import TournamentStorage


def generate_match(request: HttpRequest, match: Match) -> str:
    '''Génère un match

    Args:
        request (HttpRequest): Requete http
        match (Match): Le match

    Returns:
        str: Le match
    '''
    if match is None:
        return render_to_string('tournament/bracket/fake_match.html', {}, request)

    if match.player1 is not None:
        try: player1 = CustomUser.objects.get(id = match.player1.id)
        except: player1 = None
    else: player1 = None

    if match.player2 is not None:
        try: player2 = CustomUser.objects.get(id = match.player2.id)
        except: player2 = None
    else: player2 = None

    if match.id is not None:
        try: match_obj = Game.objects.filter(id = match.id).first()
        except: match_obj = None
    else: match_obj = None


    return render_to_string(
        'tournament/bracket/match.html',
        {
            'name1': player1.username if player1 is not None else '',
            'name2': player2.username if player2 is not None else '',
            'score1': match_obj.game_participate.score_player1 if match_obj is not None else '&nbsp;',
            'score2': match_obj.game_participate.score_player2 if match_obj is not None else '&nbsp;',
            'cls1': ' '.join(
                (['winner'] if match.player1 == match.winner and match.winner != None else []) +
                (['loser'] if match.player1 != match.winner and match.winner != None else []) +
                (['no-background'] if match.player1 is None else [])
            ),
            'cls2': ' '.join(
                (['winner'] if match.player2 == match.winner and match.winner != None else []) +
                (['loser'] if match.player2 != match.winner and match.winner != None else []) +
                (['no-background'] if match.player2 is None else [])
            )
        },
        request
    )


def generate_round(request: HttpRequest, round: list[IMatch]) -> str:
    '''Génère un tour

    Args:
        request (HttpRequest): Requete http
        round (list[IMatch]): Liste des matchs du tour

    Returns:
        str: Le tour
    '''
    spacer = render_to_string('tournament/bracket/spacer.html', {}, request)
    matches = [generate_match(request, match) for match in round]

    return render_to_string('tournament/bracket/round.html', {'rounds': spacer.join(matches)}, request)


def generate_winner(request: HttpRequest, winner: Player) -> str:
    '''Génère le gagnant du tournoi

    Args:
        request (HttpRequest): Requete http
        winner (Player): Le gagnant du tournoi

    Returns:
        str: Le gagnant du tournoi
    '''
    winner_str = render_to_string(
        'tournament/bracket/winner.html',
        {
            'name': winner.username if winner is not None else '&nbsp;',
            'cls': 'no-background' if winner is None else ''
        },
        request
    )
    return render_to_string('tournament/bracket/round.html', {'rounds': winner_str}, request)


def _generate_tournament(request: HttpRequest, tournament: TournamentLogic) -> str:
    '''Génère l'arbre du tournoi

    Args:
        request (HttpRequest): Requete http
        tournament (TournamentLogic): Le tournoi

    Returns:
        str: L'arbre du tournoi
    '''
    levels = []
    pile = [tournament.bracket]
    new_pile = []

    while pile:
        element = pile.pop(0)

        if isinstance(element, Bracket):
            if isinstance(element.bracket1, (Bracket, Match)):
                new_pile.append(element.bracket1)

            if isinstance(element.bracket2, (Bracket, Match)):
                new_pile.append(element.bracket2)

        if not pile:
            pile = new_pile.copy()
            if new_pile: levels.append(new_pile)
            new_pile = []

    levels.reverse()

    if len(levels[0]) != len(levels[1] * 2):
        new_level0 = []

        for element in levels[1]:
            if isinstance(element, Bracket):
                if isinstance(element.bracket1, Match):
                    new_level0 += [levels[0].pop(0)]

                elif isinstance(element.bracket1, Bracket):
                    new_level0 += [None]

                else:
                    new_level0 += [None]


                if isinstance(element.bracket2, Match):
                    new_level0 += [levels[0].pop(0)]

                elif isinstance(element.bracket2, Bracket):
                    new_level0 += [None]

                else:
                    new_level0 += [None]


            else:
                new_level0 += [None, None]

        levels[0] = new_level0 + levels[0]

    levels.append([tournament.bracket])


    rounds = [generate_round(request, round) for round in levels] + [generate_winner(request, tournament.bracket.winner)]

    return render_to_string('tournament/bracket/tournament.html', {'rounds': '\n'.join(rounds)}, request)


@login_required
def tournament_manager(request: HttpRequest, id: int) -> HttpResponse:
    '''Affiche la page de gestion du tournois
        
        Args:
            request (HttpRequest): Requete http
            id (int): id du tournois

        Returns:
            HttpResponse: Reponse Http de la page demandee
    '''
    tournament = Tournament.objects.get(id=id)
    participants = _get_tournament_participants(tournament)

    game_count = Game.objects.filter(tournament=tournament).count()
    if tournament.ongoing() and not tournament.terminated() and game_count == 0:
        start_tournament(tournament, participants)

    try:
        tournament_logic = TournamentStorage.load_tournament(tournament.tournament_status.path)
        tournament_res = _generate_tournament(request, tournament_logic)

    except:
        tournament_res = ''

    context = {
        'tournament': tournament,
        'organisator': tournament.organisator,
        'creator': tournament.creator,
        'tree': tournament_res,
        'in_tournament': request.user in participants,
        'ongoing': tournament.ongoing(),
        'show_buttons': (
            request.user == tournament.creator and
            (not tournament.ongoing()) and
            (not tournament.terminated()) and
            (not tournament.has_started_in_theory())
        ),
        'has_started_in_theory': tournament.has_started_in_theory(),
    }

    return render(request, 'tournament/tournament_manager.html', context)


def _get_tournament_participants(tournament:Tournament)->list[CustomUser]:
    '''Permet d'obtenir la liste des participants du tournois
        Args:
            tournament (Tournament): le tournois

        Returns:
            list[CustomUser]: la liste des user participants
    '''
    participate = ParticipateTournament.objects.filter(tournament=tournament)
    participants = [entry.person for entry in participate]
    return participants


@login_required
def tournament_join(request: HttpRequest, id_tournament:int) -> HttpResponse:
    '''Permet de rejoindre un tournois

        Args:
            request (HttpRequest): Requete Http
            id_tournament (int): id du tournois

        Returns:
            HttpResponse: Reponse Http confirmant ou non que l'on a rejoint le tournois
    '''
    ret = None
    tournament = get_object_or_404(Tournament, id=id_tournament)

    if tournament.has_started_in_theory() == True:
        ret = HttpResponseNotifError('Les inscriptions pour ce tournoi sont terminées')

    if len(ParticipateTournament.objects.filter(person=request.user, tournament=tournament).all()) < 1:
        ParticipateTournament.objects.create(
            person = request.user,
            tournament = tournament,
            win = False,
        )
        ret = HttpResponse('''
            <script>
                    window.location.reload();
            </script>
            ''')
    else:
        ret = HttpResponseNotifError('Vous participez deja au tournois')
    
    return ret

@login_required
def tournament_player_list(request: HttpRequest) -> HttpResponse:
    '''Permet de lister les joueurs du tournois

        Args:
            request (HttpRequest): Requete Http

        Returns:
            HttpResponse: Reponse Http contenant la liste
    '''
    ret = HttpResponseBadRequest()
    if request.method == 'GET':
        if (id_tournament := request.GET.get('id')) is None: return HttpResponseNotifError('Une erreur est survenue')
        try:
            tournament = Tournament.objects.get(id = id_tournament)
            listplayers = CustomUser.objects.filter(participatetournament__tournament__id = id_tournament).all()
            ret = render(request, 'reusable/tournament_player_list.html', {'players': listplayers, 'tournament_unstarted': (not tournament.ongoing()) and tournament.creator.id == request.user.id})
        
        except: ret = HttpResponseNotifError('Une erreur est survenue')

    return ret
