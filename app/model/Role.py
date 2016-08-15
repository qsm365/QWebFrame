# -*- coding:utf-8 -*-

from . import db
from Privilege import Privilege

privilege_role = db.Table('privilege_role',
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),
                       db.Column('privilege_id', db.Integer(), db.ForeignKey('privilege.id')))


#角色
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    alias = db.Column(db.String(255))
    privileges = db.relationship('Privilege', secondary=privilege_role,
                            backref=db.backref('roles', lazy='dynamic'))

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'alias': self.alias
        };