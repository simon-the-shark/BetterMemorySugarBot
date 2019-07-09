from functools import wraps

from django.conf import settings
from django.http import HttpResponseForbidden


def secret_key_required(view_func):
    """ authorization decorator """
    @wraps(view_func)
    def _required(requst,*args,**kwargs):
        their_key = requst.GET.get("key","")
        if their_key == settings.SECRET_KEY:
            return view_func(requst,*args,**kwargs)
        else:
            return HttpResponseForbidden()
    return _required