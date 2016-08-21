# -*- coding:utf-8 -*-

from sqlalchemy import or_

from model import db
from model.User import User
import re


class UserService:
    email_check = re.compile(r'^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$')

    def __init__(self):
        pass

    @staticmethod
    def is_exist(username):
        if User.query.filter_by(name=username).first():
            return True
        else:
            return False

    def check_user(self,username,password,email):
        if username and password and email:
            if self.email_check.match(email):
                if not self.is_exist(username):
                    return True
        return False

    @staticmethod
    def add_user(username,password,email):
        u = User(name=username,password=password,email=email,active=1,login_count=0)
        db.session.add(u)
        db.session.commit()

    @staticmethod
    def get_user(query):
        u = User.query.filter(or_(User.name.like("%" + query + "%") if query is not None else "",
                                  User.email.like("%" + query + "%") if query is not None else ""))
        return u

    @staticmethod
    def del_user(id):
        u = User.query.get(id)
        db.session.delete(u)
        db.session.commit()

    @staticmethod
    def mod_user(id, password, email):
        u = User.query.get(id)
        if password:
            u.password = password
        if email:
            u.email = email
        db.session.commit()

    @staticmethod
    def check_token(token):
        u = User.query.filter(User.token==token).all()
        if u:
            return True
        else:
            return False