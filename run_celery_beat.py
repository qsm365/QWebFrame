# -*- coding:utf-8 -*-

from __future__ import absolute_import, unicode_literals

from app import decorator
from celery.bin import beat

if __name__ == '__main__':
    beat = beat.beat(app=decorator.task.celery)
    options = {
        'loglevel': 'INFO',
        'scheduler_cls': 'app.scheduler.DatabaseScheduler'
    }
    beat.run(**options)