from django.http import FileResponse, HttpRequest, HttpResponseNotFound, HttpResponse
from ..decorators import login_required, request_type, RequestType
from ...models import CustomUser

@login_required
@request_type(RequestType.GET)
def header_pfp(request: HttpRequest) -> FileResponse:
    '''Controlleur de l'image de profil dans le header

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        FileResponse: Réponse HTTP à la requête de l'image de profil
    '''
    if request.user.profile_picture:
        return FileResponse(request.user.profile_picture)

    return HttpResponseNotFound()


@login_required
@request_type(RequestType.GET)
def get_pfp(request: HttpRequest) -> FileResponse:
    '''Controlleur de l'image de profil

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        FileResponse: Réponse HTTP à la requête de l'image de profil
    '''
    try:
        id_user = int(request.GET.get('id'))
        user = CustomUser.objects.get(id = id_user)
        ret = FileResponse(user.profile_picture)

    except:
        ret = HttpResponseNotFound()

    return ret


@login_required
@request_type(RequestType.GET)
def header_profile_name(request: HttpRequest) -> HttpResponse:
    '''Controlleur du nom d'utilisateur dans le header

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Réponse HTTP à la requête du nom d'utilisateur
    '''
    if not request.user.is_authenticated: return ''

    return HttpResponse(f'{request.user.username}')
