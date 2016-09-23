# -*- coding:utf-8 -*-

from . import db
from Role import Role


# 用户
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    email = db.Column(db.String(255))
    token = db.Column(db.String(255))
    login_count = db.Column(db.Integer)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship("Role")

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'active': self.active,
            'email' : self.email,
            'login_count' : self.login_count,
            'role_id': self.role_id,
            'role_name': self.role.name if self.role else None,
            'role_alias': self.role.alias if self.role else None
        }