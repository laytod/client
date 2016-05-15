from functools import wraps
from flask import request, abort
from cameraPi import app


def require_api_key(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        if request.headers.get('api-key') == app.api_key:
            return fn(*args, **kwargs)
        else:
            abort(401)
    return decorated
