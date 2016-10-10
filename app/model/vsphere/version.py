# -*- coding:utf-8 -*-

from .. import db

class Version(db.Model):
    __tablename__ = 'vsphere_version'

    id = db.Column(db.Integer, primary_key=True)
    synctime = db.Column(db.DateTime)

