# -*- coding:utf-8 -*-

from sqlalchemy import or_

from model import db
from model.User import User
from model.Role import Role
import re


class UserService:
    email_check = re.compile(r'^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$')

    default_role_id = 2

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
    def add_user(username, password, email, role_id=default_role_id, active=1):
        u = User(name=username, password=password, email=email, active=active, login_count=0)
        r = Role.query.get(role_id)
        if r:
            u.role = r
        db.session.add(u)
        db.session.commit()

    @staticmethod
    def get_users(query):
        u = User.query.filter(or_(User.name.like("%" + query + "%") if query is not None else "",
                                  User.email.like("%" + query + "%") if query is not None else ""))
        return u

    @staticmethod
    def get_user(user_id):
        u = User.query.get(user_id)
        return u

    @staticmethod
    def del_user(user_id):
        u = User.query.get(user_id)
        db.session.delete(u)
        db.session.commit()

    @staticmethod
    def mod_user(user_id, password, email, role_id, active):
        u = User.query.get(user_id)
        if password:
            u.password = password
        if email:
            u.email = email
        if role_id:
            r = Role.query.get(role_id)
            if r:
                u.role = r
        if active != None:
            u.active = active
        db.session.commit()

    @staticmethod
    def check_token(token):
        u = User.query.filter(User.token==token)
        if u:
            return u.first().id
        else:
            return

    @staticmethod
    def has_privilege(user_id, privilege_name, rw):
        r = User.query.get(user_id).role
        rp = r.privileges.filter_by(privilege_name=privilege_name).first()
        if rp:
            if rp.rw >= rw:
                return True
        return False
