# -*- coding:utf-8 -*-

from .. import db
from datetime import datetime

class Version(db.Model):
    __tablename__ = 'vsphere_version'

    id = db.Column(db.Integer, primary_key=True)
    synctime = db.Column(db.DateTime, default=datetime.now())

