# -*- coding:utf-8 -*-

from model import db
from model.Role import Role
from model.Privilege import Privilege


class PrivilegeService:

    def __init__(self):
        pass

    @staticmethod
    def add_privilege(name,alias,read,write):
        p0 = Privilege(name=unicode(name), alias=unicode(alias), read=False, write=False)
        p1 = Privilege(name=unicode(name), alias=unicode(alias), read=True, write=False)
        p2 = Privilege(name=unicode(name), alias=unicode(alias), read=True, write=True)
        db.session.add(p0)
        db.session.add(p1)
        db.session.add(p2)
        rs = Role.query.all()
        for r in rs:
            if read and write:
                r.privileges.append(p2)
            elif read:
                r.privileges.append(p1)
            else:
                r.privileges.append(p0)
        db.session.commit()

    @staticmethod
    def del_privilege(id):
        p = Privilege.query.get(id)
        db.session.delete(p)
        db.session.commit()

    @staticmethod
    def mod_privilege(id,alias):
        p = Privilege.query.get(id)
        p.alias = unicode(alias)
        db.session.commit()

    @staticmethod
    def get_privilege(role_id):
        r = Role.query.get(role_id)
        ps = r.privileges
        return ps

    @staticmethod
    def link_role_privilege(role_id, privilege_name, read, write):
        r = Role.query.get(role_id)
        ps = r.privileges
        for i in range(len(ps)):
            p = ps.pop()
            if p.name == privilege_name:
                p = Privilege.query.filter(Privilege.name == privilege_name, Privilege.read == read,
                                           Privilege.write == write).first()
            ps.append(p)
        r.privileges = ps
        db.session.commit()
