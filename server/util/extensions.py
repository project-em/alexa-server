from functools import wraps
from flask import g, request, redirect, url_for

def session_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('Authorization', None) == None:
            return 'no session', 403
        return f(request.headers['Authorization'], request*args, **kwargs)
    return decorated_function