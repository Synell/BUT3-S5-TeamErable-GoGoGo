from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from ..decorators import login_required, request_type, RequestType

@login_required
@request_type(RequestType.GET)
def legalmention(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page de mentions légales

    Args:
        request (HttpRequest): La requête HTTP

    Returns:
        HttpResponse: La réponse HTTP à la requête de mentions légales
    '''
    return render(request, 'footer/legalmention.html')
