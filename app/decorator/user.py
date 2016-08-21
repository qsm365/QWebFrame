# -*- coding:utf-8 -*-

from functools import wraps
from flask import session,redirect,url_for,request
from .. import app

from ..user_service import UserService


def login_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            app.logger.info("login require check")
            if session.get('token') is None:
                if request.cookies.get('token') is None:
                    app.logger.info('not login,goto login')
                    return redirect(url_for('login'))
                else:
                    app.logger.info('get token from cookie,make a check')
                    token = request.cookies.get('token')
                    if UserService.check_token(token):
                        app.logger.info('token ok,get login')
                        session['token']=token
                        return f(*args, **kwargs)
                    else:
                        app.logger.info('token not existes,goto login')
                        return redirect(url_for('login'))
            else:
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