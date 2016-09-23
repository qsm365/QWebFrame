# -*- coding:utf-8 -*-

from .. import db


# 项目主办部门
class Contacts(db.Model):
    __tablename__ = 'project_department'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    phone = db.Column(db.String(50))
    email = db.Column(db.String(50))
