# -*- coding:utf-8 -*-

from __future__ import absolute_import, unicode_literals

from app import decorator
from celery.bin import worker

if __name__ == '__main__':
    worker = worker.worker(app=decorator.task.celery)
    options = {
        'loglevel': 'INFO'
    }
    worker.run(**options)