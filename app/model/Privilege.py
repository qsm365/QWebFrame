# -*- coding:utf-8 -*-

from . import db


#权限
class Privilege(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80))
    alias = db.Column(db.String(255))
    read = db.Column(db.Boolean())
    write = db.Column(db.Boolean())

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'alias': self.alias,
            'read':self.read,
            'write':self.write
        };