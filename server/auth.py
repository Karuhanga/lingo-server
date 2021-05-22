import functools

from django.conf import settings
from django.http import HttpRequest, JsonResponse


def has_auth_token(view_func):
    @functools.wraps(view_func)
    def wrapper(request: HttpRequest, *args, **kwargs):
        if not (request.headers.get('Authorization') == f"Bearer {settings.AUTH_CODE}"):
            return JsonResponse(dict(message="Unauthorized"), status=401)
        return view_func(request, *args, **kwargs)

    return wrapper
