# -*- coding:utf-8 -*-

from . import db
import datetime

class LoginHistory(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    login_at = db.Column(db.DateTime())
    name = db.Column(db.String(255))
    login_ip = db.Column(db.String(255))

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'login_at': datetime.datetime.strftime(self.login_at,'%Y-%m-%d %H:%M:%S'),
            'name': self.name,
            'login_ip': self.login_ip
        };