# -*- coding:utf-8 -*-

from functools import wraps
from flask import session, redirect, url_for,request
from .. import app

from ..user_service import UserService


def login_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            app.logger.debug("login require check")
            if session.get('token') is None:
                if request.cookies.get('token') is None:
                    app.logger.debug('not login,goto login')
                    return redirect(url_for('login'))
                else:
                    app.logger.debug('get token from cookie,make a check')
                    token = request.cookies.get('token')
                    user_id = UserService.check_token(token)
                    if user_id:
                        app.logger.debug('token ok,get login')
                        session['token']=token
                        session['userId']=user_id
                        return f(*args, **kwargs)
                    else:
                        app.logger.debug('token not existes,goto login')
                        return redirect(url_for('login'))
            else:
                return f(*args, **kwargs)
        return decorated_function
    return decorator

def privilege(privilegeName):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session['userId']
            app.logger.info("privilege check:uid-"+str(user_id)+";privilege-"+privilegeName)

            if request.method=='GET':
                app.logger.info("privilege check read")
                if UserService.has_privilege(user_id,privilegeName, 1):
                    return f(*args, **kwargs)
                else:
                    return u'权限不足',401
            elif request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE' \
                    or request.method == 'LINK' or request.method == 'UNLINK':
                app.logger.info("privilege check write")
                if UserService.has_privilege(user_id,privilegeName, 2):
                    return f(*args, **kwargs)
                else:
                    return u'权限不足',401
        return decorated_function
    return decorator