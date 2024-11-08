from django.http import HttpRequest, HttpResponseBadRequest
from typing import Callable
from enum import StrEnum

class RequestType(StrEnum):
    '''Enum des types de requetes'''

    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'
    TRACE = 'TRACE'
    CONNECT = 'CONNECT'


def request_type(*request_types: RequestType) -> Callable:
    '''Décorateur permettant de valider si la requête est de certains types

    Args:
        *request_types (RequestType): Les types de requête

    Returns:
        Callable: Fonction décorée
    '''

    rtypes = [rt.value for rt in request_types]

    def decorator(f: Callable) -> Callable:
        def wrapper(request: HttpRequest, *args, **kwargs) -> Callable:
            return f(request, *args, **kwargs) if request.method in rtypes else HttpResponseBadRequest()
        return wrapper
    return decorator
