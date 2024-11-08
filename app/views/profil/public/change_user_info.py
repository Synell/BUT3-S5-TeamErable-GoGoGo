# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpRequest
from ...decorators import login_required, request_type, RequestType
from ....http import HttpResponseNotifSuccess

@login_required
@request_type(RequestType.POST)
def change_user_info(request: HttpRequest) -> HttpResponse:
    '''Controleur de la modification des informations de l'utilisateur
    Args:
        request (HttpRequest): Requete HTTP

    Returns:
        HttpResponse: Reponse HTTP de la modification des informations de l'utilisateur
    '''
    name = request.POST.get('username')
    email = request.POST.get('email')

    if name:
        request.user.username = name
    if email:
        request.user.email = email

    request.user.save()
    return HttpResponseNotifSuccess('Les informations ont bien été modifiées.')
