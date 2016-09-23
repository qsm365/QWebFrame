# -*- coding:utf-8 -*-

from .. import db


# 项目主办部门
class Department(db.Model):
    __tablename__ = 'project_department'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    leader1_id = db.Column(db.Integer, db.ForeignKey('project_contacts.id'))
    leader1 = db.relationship("Contacts")
    leader2_id = db.Column(db.Integer, db.ForeignKey('project_contacts.id'))
    leader2 = db.relationship("Contacts")

