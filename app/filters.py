# -*- coding:utf-8 -*-

from flask import Blueprint
from . import app

filterProfile = Blueprint('filterProfile', __name__)


@app.template_filter('adjustnum_k')
def adjustnum_filter(s):
    if s<1000:
        return str(s)+' K'
    elif s<1000000:
        return str(round(s/1024.0,2))+' M'
    elif s<1000000000:
        return str(round(s/1024.0/1024.0,2))+' G'
    else:
        return str(round(s / 1024.0 / 1024.0/ 1024.0, 2)) + ' T'


@app.template_filter('adjustnum')
def adjustnum_filter(s):
    s = s/1024;
    if s<1024:
        return str(s)+' K'
    elif s<1048576:
        return str(round(s/1024.0,2))+' M'
    elif s<1073741824:
        return str(round(s/1024.0/1024.0,2))+' G'
    else:
        return str(round(s / 1024.0 / 1024.0/ 1024.0, 2)) + ' T'


@app.template_filter('percentage')
def percentage_filter(s):
    return str(round(s*100,2))


@app.template_filter('average')
def average_filter(s):
    if len(s) > 0:
        return round(sum(s) / float(len(s)), 2)
    else:
        return 0


@app.template_filter('max')
def max_filter(s):
    if s:
        return max(s)
    else:
        return 0


@app.template_filter('notnone')
def notnone_filter(s):
    if s:
        return s
    else:
        return '-'