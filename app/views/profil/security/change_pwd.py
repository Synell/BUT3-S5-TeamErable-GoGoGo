from ...decorators import login_required, request_type, RequestType
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login
from ....http import HttpResponseNotifError, HttpResponseNotifSuccess

def _set_password(old_pwd, new_pwd, request) -> HttpResponse:
    '''Fonction qui permet de changer le mot de passe de l'utilisateur si l'ancien mdp etait correct

    Args:
        old_pwd (str): ancien mot de passe
        new_pwd (str): nouveau mot de passe
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Réponse HTTP de la modification du mot de passe de l'utilisateur
    '''
    validate_password(new_pwd)
    ret = HttpResponseNotifError('L\'ancien mot de passe est incorrect.')
    if request.user.check_password(old_pwd):
        request.user.set_password(new_pwd)
        request.user.save()
        request.user = authenticate(username=request.user.username, password=new_pwd)        
        ret = HttpResponseNotifSuccess('Le mot de passe a bien été modifié. Rechargement de la page...') 
        login(request, request.user)   
    return ret
        


@login_required
@request_type(RequestType.POST)
def change_pwd(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la modification du mot de passe de l'utilisateur

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Réponse HTTP de la modification du mot de passe de l'utilisateur
    '''
    ret: HttpResponse = HttpResponseNotifError('Une erreur est survenue.')
    old_pwd = request.POST.get('old-pwd')
    new_pwd = request.POST.get('new-pwd')
    confirm_new_pwd = request.POST.get('new-pwd-confirm')

    passwords_not_null = False 
    if request.user and old_pwd and new_pwd and confirm_new_pwd:
        passwords_not_null = True
    if passwords_not_null and new_pwd == confirm_new_pwd:
        try:
            ret = _set_password(old_pwd, new_pwd, request)
        except Exception as e:
            ret = HttpResponseNotifError('Le mot de passe n\'est pas assez sécurisé.')
    else: 
        ret = HttpResponseNotifError('Les mots de passe ne correspondent pas.')
    
    return ret