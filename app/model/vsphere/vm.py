# -*- coding:utf-8 -*-

from .. import db


class VM(db.Model):
    __tablename__ = 'vsphere_vm'

    version = db.Column(db.Integer, primary_key=True)
    vmid = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50))
    parentid = db.Column(db.String(20))
    parent = db.Column(db.String(50))
    state = db.Column(db.String(20))
    cpu = db.Column(db.Integer)
    memory = db.Column(db.Integer)
    os = db.Column(db.String(100))
    hostid = db.Column(db.String(20))
    committed = db.Column(db.BigInteger)
    uncommitted = db.Column(db.BigInteger)
    datastoreid = db.Column(db.String(20))
    datastore = db.Column(db.String(50))
