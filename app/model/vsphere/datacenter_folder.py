# -*- coding:utf-8 -*-

from .. import db


class DatacenterFolder(db.Model):
    __tablename__ = 'vsphere_datacenter_folder'

    version = db.Column(db.Integer, primary_key=True)
    folderid = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50))
    datacenterid = db.Column(db.String(20))
    datacenter = db.Column(db.String(20))
    type = db.Column(db.String(20))