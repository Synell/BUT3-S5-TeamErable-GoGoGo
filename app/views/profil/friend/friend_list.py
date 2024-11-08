from django.shortcuts import render
from ...decorators import login_required, request_type, RequestType
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest

@login_required
@request_type(RequestType.GET, RequestType.POST)
def friend_list(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la liste d'amis de l'utilisateur

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Réponse HTTP de la liste d'amis de l'utilisateur
    '''
    ret: HttpResponse = HttpResponseBadRequest()

    if request.method == 'GET':
        listfriends = request.user.friends.all()
        ret = render(request, 'reusable/friend_list.html', {'friends': listfriends})

    return ret

