import os
from django.http import HttpResponse, HttpRequest
from ...decorators import login_required, request_type, RequestType
from ....http import HttpResponseNotifError, HttpResponseNotifSuccess

def _remove_pfp(path: str) -> None:
    '''Supprime la photo de profil d'un utilisateur

    Args:
        path (str): Chemin de la photo de profil
    '''
    if path:
        try: os.remove(path)
        except: pass


@login_required
@request_type(RequestType.POST)
def change_pfp(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la modification de la photo de profil de l'utilisateur

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Réponse HTTP de la modification de la photo de profil de l'utilisateur
    '''
    ret: HttpResponse = HttpResponseNotifError('Une erreur est survenue.')
    MAX_SIZE =  2097152 # 2 * 1024 * 1024 = 2097152 (2MB)

    pfp = request.FILES.get('pfp')
    if pfp and pfp.size > MAX_SIZE:
        ret = HttpResponseNotifError('La photo de profil ne doit pas dépasser 2 Mo.')
    elif pfp :
        _remove_pfp(request.user.profile_picture.path if request.user.profile_picture else None)

        request.user.profile_picture = pfp
        request.user.save()

        ret = HttpResponseNotifSuccess('La photo de profil a bien été modifiée.')
    else:
        ret: HttpResponse = HttpResponseNotifError('Nous n''avons pas reussi a lire votre fichier.')
    return ret