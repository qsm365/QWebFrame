# -*- coding:utf-8 -*-

from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

from app.base_view import baseProfile
app.register_blueprint(baseProfile)

from app.vsphere_view import vsphereProfile
app.register_blueprint(vsphereProfile)

from app.filters import filterProfile
app.register_blueprint(filterProfile)