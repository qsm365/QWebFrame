# -*- coding:utf-8 -*-

from .. import db


class Host(db.Model):
    __tablename__ = 'vsphere_host'

    version = db.Column(db.Integer, primary_key=True)
    hostid = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50))
    parentid = db.Column(db.String(20))
    parent = db.Column(db.String(50))
    cpu = db.Column(db.Integer)
    memory = db.Column(db.Integer)
    vendor = db.Column(db.String(50))
    model = db.Column(db.String(50))