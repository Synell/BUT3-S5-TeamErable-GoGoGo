from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from ...decorators import login_required, request_type, RequestType

@login_required
@request_type(RequestType.GET)
def profile(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page de profil

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Réponse HTTP de la page de profil
    '''

    return render(request, 'profile/profile.html', {'user': request.user, 'friends': request.user.friends.all()})


