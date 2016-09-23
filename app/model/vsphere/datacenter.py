# -*- coding:utf-8 -*-

from .. import db


class Datacenter(db.Model):
    __tablename__ = 'vsphere_datacenter'

    version = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50))
