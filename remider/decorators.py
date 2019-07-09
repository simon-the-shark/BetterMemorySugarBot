from functools import wraps

from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils.translation import LANGUAGE_SESSION_KEY


def secret_key_required(view_func):
    """ authorization decorator """

    @wraps(view_func)
    def _required(request, *args, **kwargs):
        their_key = request.GET.get("key", "")
        if their_key == settings.SECRET_KEY:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    return _required


def set_language_to_LANGUAGE_CODE(view_func):
    """ setting language to LANGUAGE_CODE decorator """

    @wraps(view_func)
    def _set(request, *args, **kwargs):
        request.session[LANGUAGE_SESSION_KEY] = settings.LANGUAGE_CODE
        return view_func(request, *args, **kwargs)

    return _set
