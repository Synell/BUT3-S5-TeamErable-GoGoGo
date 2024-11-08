from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from ...forms.ConnectForm import ConnectForm
from ..decorators import login_required, logout_required, request_type, RequestType
from ...http import HttpResponseNotifError


@logout_required
@request_type(RequestType.GET, RequestType.POST)
def login_(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page de connexion

    Args:
        request (HttpRequest): La requête HTTP

    Returns:
        HttpResponse: La réponse HTTP à la requête de connexion
    '''

    ret: HttpResponse = HttpResponseNotifError('Le mot de passe ou le nom d\'utilisateur est incorrect.')

    if request.method == RequestType.GET.value:
        ret = render(request, 'connection/login.html')
    
    elif request.method == RequestType.POST.value:
        form = ConnectForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
            if user:
                login(request, user)
                ret = HttpResponseRedirect('/')
        
    return ret



@login_required
@request_type(RequestType.GET, RequestType.POST)
def logout_(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page de déconnexion

    Args:
        request (HttpRequest): La requête HTTP

    Returns:
        HttpResponse: La réponse HTTP à la requête de déconnexion
    '''

    logout(request)
    return HttpResponseRedirect('/login')
