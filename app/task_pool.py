# -*- coding:utf-8 -*-

from decorator.task import celery
from vsphere_sync import VsphereSync


class TaskPool:

    def __init__(self):
        pass

    @staticmethod
    @celery.task
    def test(a, b):
        return a + b

    @staticmethod
    @celery.task
    def test2(a, b):
        return a * b

    @staticmethod
    @celery.task
    def sync_vsphere():
        #vsphereSync = VsphereSync()
        #vsphereSync.sync()
        return "vsphere sync success"
