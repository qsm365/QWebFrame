# -*- coding:utf-8 -*-

from functools import wraps
from .. import app


def login_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            app.logger.info("login require check")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def privilege(privilegeName):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            app.logger.info("privilege check")
            return f(*args, **kwargs)
        return decorated_function
    return decorator