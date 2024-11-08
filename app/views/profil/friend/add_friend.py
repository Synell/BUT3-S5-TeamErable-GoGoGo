from ...decorators import login_required, request_type, RequestType
from django.http import HttpResponse, HttpRequest
from ....models import CustomUser
from ....http import HttpResponseNotifError, HttpResponseNotifSuccess

@login_required
@request_type(RequestType.GET)
def add_friend(request: HttpRequest) -> HttpResponse:
    '''Controlleur de l'ajout d'un ami à l'utilisateur

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Réponse HTTP de l'ajout d'un ami à l'utilisateur
    '''
    ret: HttpResponse = HttpResponseNotifError('Une erreur est survenue.')

    friend_id = request.GET.get('id')

    if friend_id is not None:
        friend = CustomUser.objects.get(id = friend_id)
        if not request.user.friends.filter(id = friend_id).exists() and friend:
            request.user.friends.add(friend)
            ret = HttpResponseNotifSuccess(f'{friend.username} a été ajouté à vos amis.')

    return ret
