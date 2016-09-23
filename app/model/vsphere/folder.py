# -*- coding:utf-8 -*-

from .. import db


class Folder(db.Model):
    __tablename__ = 'vsphere_folder'

    version = db.Column(db.Integer, primary_key=True)
    folderid = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50))
    parentid = db.Column(db.String(20))
    parent = db.Column(db.String(50))
    type = db.Column(db.String(20))
