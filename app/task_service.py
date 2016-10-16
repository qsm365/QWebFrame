# -*- coding: utf-8 -*-

import task_pool
from decorator.task import celery
from model.Scheduler import TaskHistory
from .model import db
import datetime
from task_pool import TaskPool


class TaskService:

    def __init__(self):
        pass

    @staticmethod
    def add_task(name, task, args, kwargs):
        if task[0:8] == "TaskPool":
            a_task = eval(str(task)+".apply_async(args=args,kwargs=kwargs)")
            if not args:
                args = '[]'
            if not kwargs:
                kwargs = '{}'
            th = TaskHistory(id=a_task.id, name=name, date_start=datetime.datetime.utcnow(), task=task)
            db.session.add(th)
            db.session.commit()
