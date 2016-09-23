# -*- coding:utf-8 -*-

from .. import db


class Network(db.Model):
    __tablename__ = 'vsphere_network'

    version = db.Column(db.Integer, primary_key=True)
    networkid = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50))
    parentid = db.Column(db.String(20))
    parent = db.Column(db.String(50))
    networktype = db.Column(db.String(45))
