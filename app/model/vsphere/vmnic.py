# -*- coding:utf-8 -*-

from .. import db


class VMNic(db.Model):
    __tablename__ = 'vsphere_vmnic'

    version = db.Column(db.Integer, primary_key=True)
    nicid = db.Column(db.String(20), primary_key=True)
    vmid = db.Column(db.String(20), primary_key=True)
    networkid = db.Column(db.String(50))
    ipaddress = db.Column(db.String(40))
    mac = db.Column(db.String(40))
    networktype = db.Column(db.String(20))
