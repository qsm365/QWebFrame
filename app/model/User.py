# -*- coding:utf-8 -*-

from . import db
from Role import Role

role_user = db.Table('role_user',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


#用户
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    email = db.Column(db.String(255))
    token = db.Column(db.String(255))
    login_count = db.Column(db.Integer)
    roles = db.relationship('Role', secondary=role_user,
                            backref=db.backref('users', lazy='dynamic'))

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'active': self.active,
            'email' : self.email,
            'login_count' : self.login_count
        }