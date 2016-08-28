# -*- coding:utf-8 -*-

from . import db

from RolePrivilege import RolePrivilege

#角色
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    alias = db.Column(db.String(255))
    privileges = db.relationship('RolePrivilege', cascade='all, delete', lazy='dynamic')

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'alias': self.alias
        }
