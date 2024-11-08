from django.http import HttpRequest

def verify_post(request: HttpRequest, key : str, message : str) -> str:
    '''Fonction permettant de valider les informations de la requête POST et de la renvoyer
    
    Args:
        request (HttpRequest): Requête HTTP
        key (str): La clef de la requête
        message (str): Le message d'exception
        
    Returns:
        str: La valeur

    Raises:
        Exception: message d'exception pris en paramêtre
    '''
    if (value := request.POST.get(key)) is None: 
        raise Exception(message)
    return value

def verify_get(request: HttpRequest, key : str, message : str) -> str:
    '''Fonction permettant de valider les informations de la requête GET et de la renvoyer

    Args:
        request (HttpRequest): Requête HTTP
        key (str): La clef de la requête
        message (str): Le message d'exception

    Returns:
        str: La valeur

    Raises:
        Exception: message d'exception pris en paramêtre
    '''
    if (value := request.GET.get(key)) is None: 
        raise Exception(message)
    return value
