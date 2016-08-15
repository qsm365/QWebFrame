# -*- coding:utf-8 -*-

from model import db
from model.Role import Role
from model.Privilege import Privilege
from model.User import User


class RoleService:

    def __init__(self):
        pass

    @staticmethod
    def add_role(name, alias):
        r = Role(name=unicode(name), alias=unicode(alias))
        ps = Privilege.query.filter(Privilege.read==False,Privilege.write==False).all()
        r.privileges = ps
        db.session.add(r)
        db.session.commit()

    @staticmethod
    def del_role(role_id):
        r = Role.query.get(role_id)
        db.session.delete(r)
        db.session.commit()

    @staticmethod
    def mod_role(role_id, alias):
        r = Role.query.get(role_id)
        if alias:
            r.alias = unicode(alias)
        db.session.commit()

    @staticmethod
    def get_role():
        r = Role.query.all()
        return r

    @staticmethod
    def link_user_role(user_id, role_id):
        u = User.query.get(user_id)
        rs = u.roles
        r = Role.query.get(role_id)
        rs.append(r)
        u.roles = rs
        db.session.commit()

    @staticmethod
    def unlink_user_role(user_id, role_id):
        u = User.query.get(user_id)
        rs = u.roles
        for i in range(len(rs)):
            r = rs.pop()
            if r.id != role_id:
                rs.append(r)
        u.roles = rs
        db.session.commit()
