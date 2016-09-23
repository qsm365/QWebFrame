# -*- coding:utf-8 -*-

from flask import request
import datetime
import re
import pytz

from . import app


class Util:

    def __init__(self):
        pass

    @staticmethod
    def get_ip_addr():
        ip1 = request.headers.get('X-Forwarded-For')
        ip2 = request.headers.get('X-Real-Ip')
        ip3 = request.remote_addr
        if ip1:
            return ip1.split(',')[0]
        elif ip2:
            return ip2.split(',')[0]
        else:
            return ip3

    @staticmethod
    def can_tune_to( v, t):
        try:
            t(v)
            return True
        except ValueError:
            return False

    @staticmethod
    def transform_to_datetime(s):
        try:
            return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None

    @staticmethod
    def transform_to_date(s):
        try:
            return datetime.datetime.strptime(s, '%Y-%m-%d')
        except ValueError:
            return None

    @staticmethod
    def check_date_str(s):
        try:
            if re.match('\d\d\d\d-\d\d-\d\d', s):
                return s
        except:
            return None
        return None

    @staticmethod
    def utc2local(d):
        local_tz = pytz.timezone(app.config.get('TIMEZONE'))
        local_dt = d.replace(tzinfo=pytz.utc).astimezone(local_tz)
        return local_tz.normalize(local_dt)
