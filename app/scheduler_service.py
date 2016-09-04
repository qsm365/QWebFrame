# -*- coding:utf-8 -*-

import time
from sqlalchemy import or_,and_

from model import db
from model.Scheduler import DatabaseSchedulerEntry,CrontabSchedule,IntervalSchedule,SchedulerHistory,Task

from decorator.task import celery

class SchedulerService:

    def __init__(self):
        pass

    def crontab(self):
        dse = DatabaseSchedulerEntry()
        dse.name = 'crontab task'
        dse.task = 'app.task_pool.test'
        dse.arguments = '[1,2]'  # json string
        dse.keyword_arguments = '{}'  # json string

        # crontab defaults to run every minute
        dse.crontab = CrontabSchedule()

        db.session.add(dse)
        db.session.commit()

    def interval(self):
        dse = DatabaseSchedulerEntry()
        dse.name = 'interval task'
        dse.task = 'app.task_pool.test'
        dse.arguments = '[1,2]'  # json string
        dse.keyword_arguments = '{}'  # json string

        # crontab defaults to run every minute
        dse.interval = IntervalSchedule(every=10, period='seconds')

        db.session.add(dse)
        db.session.commit()

    @staticmethod
    def get_tasks():
        ret = list()
        for t in celery.tasks:
            n = str(t)
            if n[0:6]!='celery':
                ret.insert(0, str(t))
        return ret

    @staticmethod
    def get_schedule_list():
        ss = DatabaseSchedulerEntry.query.all()
        return ss

    @staticmethod
    def get_task_history(query, start_at):
        ss = db.session.query(DatabaseSchedulerEntry.id).filter(or_(DatabaseSchedulerEntry.name.like("%" + query + "%") if query is not None else "",
                                                     DatabaseSchedulerEntry.task.like("%" + query + "%") if query is not None else ""))
        sh = SchedulerHistory.query.filter(SchedulerHistory.schedule_id.in_(ss),
                                           and_(SchedulerHistory.date_start >= start_at + ' 00:00:00',
                                                SchedulerHistory.date_start <= start_at + ' 23:59:59') if start_at is not None else "")
        return sh

    @staticmethod
    def get_task_detail(sh_id):
        ret = dict()
        sh = SchedulerHistory.query.get(sh_id)
        if sh:
            ret['id'] = sh.id
            ret['args'] = sh.schedule.arguments
            ret['kwargs'] = sh.schedule.keyword_arguments
            task_id = sh.task_id
            task = Task.query.filter(Task.task_id==task_id).first()
            if task:
                ret['result'] = task.result
                ret['traceback'] = task.traceback
            else:
                ret['result'] = None
                ret['traceback'] = None
            return ret
