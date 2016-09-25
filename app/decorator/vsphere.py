# -*- coding:utf-8 -*-

from functools import wraps
from flask import render_template

from ..vsphere_service import VsphereService


def get_last_version():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            version = VsphereService.get_new_version()
            if version:
                return f(version, *args, **kwargs)
            else:
                return render_template('vsphere/vsphere_nodata.html', title=u'VSphere数据尚未采集')
        return decorated_function
    return decorator