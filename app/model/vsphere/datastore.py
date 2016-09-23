# -*- coding:utf-8 -*-

from .. import db


class Datastore(db.Model):
    __tablename__ = 'vsphere_datastore'

    version = db.Column(db.Integer, primary_key=True)
    datastoreid = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50), primary_key=True)
    parentid = db.Column(db.String(20))
    parent = db.Column(db.String(50))
    capacity = db.Column(db.BigInteger)
    freespace = db.Column(db.BigInteger)
    uncommitted = db.Column(db.BigInteger)


